import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
CONNECTION = (
    "postgresql+psycopg://"
    "postgres:postgres@localhost:5432/rag"
)

def ingest_pdf():
    if not PDF_PATH:
        raise ValueError("PDF_PATH environment variable is not set.")
    
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    return documents

def chunk_documents(documents, chunk_size=1000, chunk_overlap=150):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)

def generate_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")

def store_embeddings_in_db(embeddings, chunked_documents):
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="documents",
        connection=CONNECTION,
        use_jsonb=True,
    )

    vector_store.add_documents(chunked_documents)

if __name__ == "__main__":
    documents = ingest_pdf()
    chunked_documents = chunk_documents(documents)
    embeddings = generate_embeddings()

    store_embeddings_in_db(embeddings, chunked_documents)
