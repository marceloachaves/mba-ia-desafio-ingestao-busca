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
    
    # Here you can process the documents as needed
    # for doc in documents:
    #     print(doc.page_content)  # Example: print the content of each page

    return documents

def chunk_documents(documents, chunk_size=1000, chunk_overlap=150):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)

def generate_embeddings():
    # return GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    return OpenAIEmbeddings(model="text-embedding-3-small")

def store_embeddings_in_db(embeddings, chunked_documents):
    # 4. Vector Store
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="documents",
        connection=CONNECTION,
        use_jsonb=True,
    )

    # 5. Ingestão
    vector_store.add_documents(chunked_documents)

if __name__ == "__main__":
    documents = ingest_pdf()
    chunked_documents = chunk_documents(documents)
    # generate embeddings and store them in the database as needed
    embeddings = generate_embeddings()

    store_embeddings_in_db(embeddings, chunked_documents)
