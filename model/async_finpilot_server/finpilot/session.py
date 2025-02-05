import dill
from finpilot.vectorstore import load_faiss_from_redis, create_empty_faiss, save_faiss_to_redis
from finpilot.core import get_finpilot
from finpilot.memory import LimitedMemorySaver

async def get_session_app(redis_client, session_id):
    if redis_client.exists(f"{session_id}_memory_saver"):
        memory = dill.loads(redis_client.get(f"{session_id}_memory_saver"))
        print(f"[Server Log] MEMORY LOADED FOR SESSION ID : {session_id}")

        vectorstore = load_faiss_from_redis(redis_client=redis_client, session_id=session_id)
        print(f"[Server Log] VECTORSTORE LOADED FOR SESSION ID : {session_id}")

        pilot = await get_finpilot(memory=memory, vector_store=vectorstore, session_id=session_id)
        print(f"[Server Log] APPLICATION LOADED FOR SESSION ID : {session_id}")

    else:
        memory = LimitedMemorySaver(capacity=10)
        print(f"[Server Log] MEMORY CREATED FOR SESSION ID : {session_id}")

        vectorstore = create_empty_faiss()
        print(f"[Server Log] VECTORESTORE CREATED FOR SESSION ID : {session_id}")

        pilot = await get_finpilot(memory=memory, vector_store=vectorstore, session_id=session_id)
        print(f"[Server Log] APPLICATION CREATED FOR SESSION ID : {session_id}")
        
        redis_client.set(f"{session_id}_memory_saver", dill.dumps(memory))
        redis_client.expire(f"{session_id}_memory_saver", 3600)
        print(f"[Server Log] MEMORY SAVED TO REDIS FOR SESSION ID : {session_id}")

        save_faiss_to_redis(
            redis_client=redis_client,
            session_id=session_id,
            vector_store=vectorstore
        )
        
    return pilot


def get_session_vectorstore(redis_client, session_id):
    # Redis 에서 session data 로드
    if redis_client.exists(f"{session_id}_faiss_index"):
        vectorstore = load_faiss_from_redis(redis_client=redis_client, session_id=session_id)
        print(f"[Server Log] VECTORSTORE LOADED FOR SESSION ID : {session_id}")
    else:
        memory = LimitedMemorySaver(capacity=10)
        print(f"[Server Log] MEMORY CREATED FOR SESSION ID : {session_id}")

        vectorstore = create_empty_faiss()
        print(f"[Server Log] VECTORESTORE CREATED FOR SESSION ID : {session_id}")
        
        redis_client.set(f"{session_id}_memory_saver", dill.dumps(memory))
        redis_client.expire(f"{session_id}_memory_saver", 3600)
        print(f"[Server Log] MEMORY SAVED TO REDIS FOR SESSION ID : {session_id}")

        save_faiss_to_redis(
            redis_client=redis_client,
            session_id=session_id,
            vector_store=vectorstore
        )


    return vectorstore