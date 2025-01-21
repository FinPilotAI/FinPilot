from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from Middleware.mid import TimingMiddleware, RateLimitMiddleware
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from DB import schemas, crud
from DB.database import engine, SessionLocal
from DB.models import Base, SessionID
from datetime import datetime, timezone
from dotenv import load_dotenv
from Runpod.runpod import send_question_to_runpod, send_pdf_to_runpod, send_csv_to_runpod
import uvicorn
from fastapi import File, UploadFile
import requests

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# CORS configuration (adjust as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production security
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Performance and monitoring middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TimingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# url/docs 로 기능 설명 페이지 안내
@app.get("/")
async def hello():
    return {"hello": "/docs for more info"}

# -------------------
# 데이터베이스 의존성
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------
# 유저 정보 CRUD 엔드포인트
# -------------------
@app.post("/users/", response_model=schemas.Member)
def create_or_update_user(user: schemas.MemberBase, db: Session = Depends(get_db)):
    # 현재 시간을 UTC로 설정
    current_time = datetime.now(timezone.utc)

    # 기존 유저 확인
    existing_user = crud.get_user_by_email(db=db, user_email=user.user_email)
    if existing_user:
        # 기존 유저 로그인 시간 업데이트
        updated_user = crud.update_user_login_time(db=db, user_email=user.user_email)
        return updated_user

    # 새로운 유저 생성
    new_user = crud.create_user(db=db, user_email=user.user_email)
    return new_user


@app.get("/users/", response_model=list[schemas.Member])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_email}", response_model=schemas.Member)
def read_user(user_email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db=db, user_email=user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_email}")
def delete_user(user_email: str, db: Session = Depends(get_db)):
    result = crud.delete_user(db=db, user_email=user_email)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# -------------------
# 세션 정보 CRUD 엔드포인트
# -------------------
@app.post("/sessions/", response_model=schemas.SessionID)
def create_session(session_data: schemas.SessionIDBase, db: Session = Depends(get_db)):
    try:
        # Check if the session already exists or create a new one
        new_session = crud.create_session(
            db=db,
            user_email=session_data.user_email,
            docs_id=session_data.docs_id,
        )
        return new_session
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))  # Handle invalid input
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/sessions/", response_model=list[schemas.SessionID])
def read_sessions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    sessions = crud.get_sessions(db=db, skip=skip, limit=limit)
    return sessions

@app.get("/sessions/{session_id}", response_model=schemas.SessionID)
def read_session(session_id: str, db: Session = Depends(get_db)):
    session = crud.get_session_by_id(db=db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.delete("/sessions/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    success = crud.delete_session(db=db, session_id=session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}

# -------------------
# 질문 기록 CRUD 엔드포인트 및 RunPod 연동
# -------------------
@app.post("/qnas/", response_model=schemas.QnA)
def create_qna(qna: schemas.QnACreate, db: Session = Depends(get_db)):
    """
    QnA 생성 엔드포인트:
    1. 세션 확인 또는 생성
    2. RunPod 호출 (질문과 session_id 전달)
    3. QnA 데이터 생성 및 저장
    """
    try:
        # 1. 세션이 존재하는지 확인하거나 생성
        session = crud.create_session(
            db=db,
            user_email=qna.user_email,
            docs_id=qna.docs_id,
        )

        # 2. RunPod 호출 (외부 서비스 연동) - question과 session_id 전달
        try:
            answer = send_question_to_runpod({
                "question": qna.question,
                "session_id": session.session_id,  # session_id를 RunPod에 전달
                "chat_option": qna.chat_option,   # chat_option도 함께 전달
            })
        except Exception as e:
            raise HTTPException(status_code=502, detail="Failed to communicate with RunPod")

        # 3. QnA 데이터 생성 및 저장 (session_id 및 chat_option 포함)
        new_qna = crud.create_qna(
            db=db,
            user_email=qna.user_email,
            docs_id=qna.docs_id,
            question=qna.question,
            session_id=session.session_id,
            chat_option=qna.chat_option,  # chat_option 명시적으로 전달
        )
        
        # 4. RunPod에서 받은 답변을 QnA에 추가
        new_qna.answer = answer
        db.commit()
        db.refresh(new_qna)

        return new_qna
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))  # 잘못된 입력 처리
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/pdfs/", response_model=list[schemas.PDFFile], operation_id="get_all_pdfs")
def read_pdfs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of all PDF files.
    """
    pdfs = crud.get_pdfs(db=db, skip=skip, limit=limit)
    return pdfs


@app.delete("/pdfs/{pdf_id}", operation_id="delete_single_pdf")
def delete_pdf(pdf_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific PDF file by its ID.
    """
    success = crud.delete_pdf_file(db=db, pdf_id=pdf_id)
    if not success:
        raise HTTPException(status_code=404, detail="PDF file not found")
    return {"message": "PDF file deleted successfully"}

# -------------------
# PDF 파일 CRUD 엔드포인트
# -------------------
@app.post("/pdfs/", response_model=schemas.PDFFile)
async def create_pdf(
    user_email: str,
    docs_id: str,
    file: UploadFile = File(...),  # 파일 업로드 처리
    db: Session = Depends(get_db)
):
    """
    클라이언트로부터 user_email, docs_id, PDF 파일을 받아서:
    1. session_id를 생성하거나 가져옴.
    2. PDF 파일 이름을 데이터베이스에 저장.
    3. session_id와 PDF 파일을 RunPod으로 전송.
    """
    try:
        # 1. 세션 확인 또는 생성
        session = crud.create_session(db=db, user_email=user_email, docs_id=docs_id)
        session_id = session.session_id

        # 2. 파일 이름 저장 (데이터베이스에 저장할 정보)
        file_name = file.filename

        # 3. PDF 파일 정보 생성 및 저장 (파일 이름만 저장)
        new_pdf_file = crud.create_pdf_file(
            db=db,
            user_email=user_email,
            docs_id=docs_id,
            file_name=file_name,
        )

        # 4. RunPod으로 파일과 session_id 전송
        runpod_response = send_pdf_to_runpod(file=file, session_id=session_id)

        # 5. RunPod 응답 확인 및 반환
        if runpod_response.get("status") != "success":
            raise HTTPException(status_code=502, detail="Failed to process file with RunPod")

        return {
            "message": "PDF file processed successfully",
            "session_id": session_id,
            "pdf_file": new_pdf_file,
            "runpod_response": runpod_response,
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))  # 잘못된 입력 처리
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/pdfs/", response_model=list[schemas.PDFFile])
def read_pdfs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pdfs = crud.get_pdfs(db=db, skip=skip, limit=limit)
    return pdfs

@app.delete("/pdfs/{pdf_id}")
def delete_pdf(pdf_id: int, db: Session = Depends(get_db)):
    success = crud.delete_pdf_file(db=db, pdf_id=pdf_id)
    if not success:
        raise HTTPException(status_code=404, detail="PDF file not found")
    return {"message": "PDF file deleted successfully"}

@app.get("/pdfs/", response_model=list[schemas.PDFFile])
def read_pdfs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pdfs = crud.get_pdfs(db=db, skip=skip, limit=limit)
    return pdfs

@app.delete("/pdfs/{pdf_id}")
def delete_pdf(pdf_id: int, db: Session = Depends(get_db)):
    success = crud.delete_pdf_file(db=db, pdf_id=pdf_id)
    if not success:
        raise HTTPException(status_code=404, detail="PDF file not found")
    return {"message": "PDF file deleted successfully"}

# -------------------
# CSV 파일 업로드 엔드포인트
# -------------------
@app.post("/csvs/")
async def upload_csv(
    user_email: str,
    docs_id: str,
    file: UploadFile = File(...),  # 파일 업로드 처리
    db: Session = Depends(get_db)
):
    """
    클라이언트가 업로드한 CSV 파일과 함께 user_email 및 docs_id를 받아서,
    session_id와 파일을 RunPod으로 전송.
    """
    try:
        # 1. 세션 확인 또는 생성
        session = crud.create_session(db=db, user_email=user_email, docs_id=docs_id)
        session_id = session.session_id

        # 2. 파일 형식 확인 (CSV만 허용)
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

        # 3. RunPod으로 파일과 session_id 전송
        runpod_response = send_csv_to_runpod(file=file, session_id=session_id)

        # 4. RunPod 응답 반환
        if runpod_response.get("status") != "success":
            raise HTTPException(status_code=502, detail="Failed to process CSV file with RunPod")

        return {
            "message": "CSV file processed successfully",
            "session_id": session_id,
            "runpod_response": runpod_response,
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
# -------------------
# 파이썬 서버 실행
# -------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)