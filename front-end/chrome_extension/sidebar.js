// OpenAI API (키 각자 개인의 키를 넣어주세요!!!!!!!!!!!!!!!!!!)
const OPENAI_API_KEY ="sk-proj--";  

// 문서 아이디 초기값 설정
let DOCUMENT_ID = ""; 

// 현재 활성탭을 가져와 문서 id 찾기
function getDocumentIdFromActiveTab() {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError.message);
        return;
      }

      if (!tabs.length || !tabs[0].url) {
        reject("활성 탭을 찾을 수 없습니다.");
        return;
      }

      const url = tabs[0].url;
      console.log("현재 탭 URL:", url);

      if (!url.includes("https://docs.google.com/document/")) {
        reject("Google Docs 문서 페이지가 아닙니다.");
        return;
      }

      const match = url.match(/\/d\/([a-zA-Z0-9_-]+)/); // 문서 ID 추출
      if (match) {
        resolve(match[1]);
      } else {
        reject("URL에서 Google Docs 문서 ID를 찾을 수 없습니다.");
      }
    });
  });
}

// 찾은 문서 아이디 알려주기
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const docId = await getDocumentIdFromActiveTab();
    if (docId) {
      DOCUMENT_ID = docId;
      console.log(`문서 ID 자동 추출 성공: ${DOCUMENT_ID}`);
      alert(`Google Docs 문서가 연동되었습니다.\n\n문서 ID: ${DOCUMENT_ID}`);  // 활성 탭이 구글 docs라서 정상적으로 문서 id를 가져왔을 때
    }
  } catch (error) {
    console.error("문서 ID 추출 실패:", error);
    // 지금 활성화된 탭이 구글 docs가 아니라서 문서 id를 제대로 못 가져올 때
    alert("현재 활성 탭은 Google Docs 문서 페이지가 아닙니다.\nGoogle Docs 문서를 열고 다시 시도해주세요.\n\n - 예시 URL: https://docs.google.com/document/d/문서ID/edit"); 
  }
});

// 로딩 버퍼링 스피너 제어 함수
function showLoadingSpinner() {
  const spinner = document.getElementById("loading-spinner");
  const chatContainer = document.querySelector(".chat-container");
  if (spinner) spinner.style.display = "block";
  if (chatContainer) chatContainer.classList.add("loading"); // 흐림 효과 추가
}
function hideLoadingSpinner() {
  const spinner = document.getElementById("loading-spinner");
  const chatContainer = document.querySelector(".chat-container");
  if (spinner) spinner.style.display = "none";
  if (chatContainer) chatContainer.classList.remove("loading"); // 흐림 효과 제거
}

// "Send" 버튼 클릭 이벤트
document.getElementById("send-btn").addEventListener("click", async () => {
  const userInput = document.getElementById("user-input").value.trim();
  // 사용자 메시지가 비어있는 경우 중단
  if (!userInput) {
    alert("질문을 입력해주세요.");
    return;
  }

  // 환영 메시지 숨기기
  const greetingElement = document.getElementById('greeting');
  if (greetingElement) {
    greetingElement.style.display = 'none';
  } 

  const chatBox = document.getElementById("chat-box");

  // 사용자 메시지 생성
  const userMessage = document.createElement("div");
  userMessage.classList.add("chat-message", "question"); // 사용자 메시지에 클래스 추가
  userMessage.textContent = `${userInput}`; //🧑‍💻
  chatBox.appendChild(userMessage);

  // 로딩 스피너 표시
  showLoadingSpinner();

  try {
    // GPT 호출
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-4",
        messages: [{ role: "user", content: userInput }],
      }),
    });

    if (!response.ok) throw new Error("GPT API 호출 실패");

    const data = await response.json();
    const botMessage = data.choices[0]?.message?.content || "GPT 응답 실패";

    // GPT 응답 메시지 생성
    const botMessageElement = document.createElement("div");
    botMessageElement.classList.add("chat-message", "answer"); // GPT 메시지에 클래스 추가
    botMessageElement.innerHTML = `
    <img src="icon_circle.png" alt="FinPilot Icon" width="32" height="32" style="margin-right: 3px; vertical-align: middle;">
    <span>${botMessage}</span>`; // FinPilot 로고

    chatBox.appendChild(botMessageElement);

    await appendToGoogleDoc(botMessage); // Google Docs에 추가

    chatBox.scrollTop = chatBox.scrollHeight;
  } catch (error) {
    console.error("❌ 오류:", error);
  } finally {
    // 로딩 버퍼링 스피너 숨기기
    hideLoadingSpinner();
  }

  document.getElementById("user-input").value = ""; // 메시지 입력창 초기화
});

// "Enter" 키로 전송 이벤트 구현
document.getElementById("user-input").addEventListener("keyup", (event) => {
  if (event.key === "Enter") {
    event.preventDefault(); // 기본 Enter 동작 방지
    document.getElementById("send-btn").click(); // Send 버튼 클릭 동작 실행
  }
});

// Google Docs에 답변 반영
async function appendToGoogleDoc(content) {
    try {
      const accessToken = await getAccessToken();
  
      const response = await fetch(
        `https://docs.googleapis.com/v1/documents/${DOCUMENT_ID}:batchUpdate`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            requests: [
              {
                insertText: {
                  location: { index: 1 },
                  text: `${content}\n`,
                },
              },
            ],
          }),
        }
      );
  
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`❌ Google Docs 업데이트 실패: ${errorText}`);
      }
  
      console.log("✅ Google Docs 업데이트 성공!");
    } catch (error) {
      console.error("❌ Google Docs API 오류:", error);
      alert("Google Docs 업데이트 중 문제가 발생했습니다.\n\nGoogle 로그인을 완료하고 현재 활성 탭이 Google Docs 문서 페이지인지 확인 후 다시 시도해주세요.");
    }
}

// 실시간으로 OAuth 토큰을 가져오기
async function getAccessToken() {
    return new Promise((resolve, reject) => {
      chrome.identity.getAuthToken({ interactive: true }, (token) => {
        if (chrome.runtime.lastError || !token) {
          reject(chrome.runtime.lastError || "Token을 가져올 수 없습니다.");
          return;
        }
        resolve(token);
      });
    });
}

// 환영 인사
document.addEventListener('DOMContentLoaded', () => {
  // Greeting 요소 가져오기
  const greetingElement = document.getElementById('greeting');

  // 저장된 userName 가져오기
  chrome.storage.local.get(['userName', 'isLoggedIn'], (data) => {
    if (data.isLoggedIn && data.userName) {
      // 로그인된 경우 환영 메시지 표시
      greetingElement.textContent = `${data.userName}님, 안녕하세요`;
      greetingElement.style.display = 'block';
    } else {
      // 로그인되지 않은 경우 숨기기
      greetingElement.style.display = 'none';
    }
  });
});
