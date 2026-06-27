from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from app.config import (
    CHROMA_DB_DIR,
    EMBEDDING_MODEL,
)


embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

vector_db = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings,
)

retriever = vector_db.as_retriever(
    search_kwargs={
        "k": 5
    }
)


def retrieve(question: str):

    documents = retriever.invoke(question)

    return documents