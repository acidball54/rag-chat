import os
import sys

from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

SCRIPT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.config import (
    DATA_DIR,
    CHROMA_DB_DIR,
    EMBEDDING_MODEL,
)


def load_documents():

    loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.md",
    )

    return loader.load()


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
    )

    return splitter.split_documents(documents)


def create_vector_db(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR,
    )


def main():

    print("Loading markdown files...")

    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    print("Splitting documents...")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    print("Creating vector database...")

    create_vector_db(chunks)

    print("Done!")


if __name__ == "__main__":
    main()