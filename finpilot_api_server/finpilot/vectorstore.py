# Construct Vector DB / Create retriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document

import os

import faiss
import dill
import numpy as np


def create_empty_faiss():
    docstore = InMemoryDocstore({})
    index_to_docstore_id = {}

    vector_store = FAISS(
        embedding_function = OpenAIEmbeddings(
            api_key=os.environ['OPENAI_API_KEY']
        ),
        index=faiss.IndexFlatL2(1536),
        docstore=docstore,
        index_to_docstore_id=index_to_docstore_id
    )
    return vector_store 


def load_faiss_from_redis(redis_client, session_id):
    # Restore FAISS index
    faiss_binary = redis_client.get(f"{session_id}_faiss_index")
    if not faiss_binary:
        raise ValueError(f"No FAISS index found for session '{session_id}'")
    faiss_array = np.frombuffer(faiss_binary, dtype=np.uint8)
    faiss_index = faiss.deserialize_index(faiss_array)

    # Restore FAISS Meta data
    metadata_binary = redis_client.get(f"{session_id}_faiss_metadata")
    if not metadata_binary:
        raise ValueError(f"No metadata found for session '{session_id}'")
    metadata = dill.loads(metadata_binary)
    texts = metadata['texts']
    index_to_id = metadata['index_to_id']

    # Restore FAISS vectorStore
    vectorstore = FAISS(
        embedding_function=OpenAIEmbeddings(
            api_key=os.environ['OPENAI_API_KEY']
        ),
        index=faiss_index,
        docstore=InMemoryDocstore(texts),
        index_to_docstore_id=index_to_id
    )

    return vectorstore

def save_faiss_to_redis(redis_client, session_id, vector_store : FAISS):
    faiss_buffer = faiss.serialize_index(vector_store.index)
    redis_client.set(f"{session_id}_faiss_index", faiss_buffer.tobytes())
    redis_client.expire(f"{session_id}_faiss_index", 3600)

    # save metadata
    metadata = dill.dumps({
        "texts" : vector_store.docstore._dict,
        "index_to_id" : vector_store.index_to_docstore_id
    })
    redis_client.set(f"{session_id}_faiss_metadata", metadata)
    redis_client.expire(f"{session_id}_faiss_metadata", 3600)

    print(f"FAISS VectorStore saved to Redis for session '{session_id}'.")


def add_data_to_vectorstore_and_update_redis(redis_client, session_id, vector_store : FAISS, data : list[Document]):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300, chunk_overlap=50
    )
    doc_splits = text_splitter.split_documents(data)
    new_texts = [doc.page_content for doc in doc_splits]

    vector_store.add_texts(new_texts)
    save_faiss_to_redis(
        redis_client=redis_client,
        session_id=session_id,
        vector_store=vector_store
    )

    print(f"VectorStore updated and saved to Redis for Session '{session_id}'.")