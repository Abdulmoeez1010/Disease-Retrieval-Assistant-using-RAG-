import pandas as pd
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

VECTOR_DB_PATH = "data/faiss_symptom_index"
CSV_PATH = "data/cleaned_symptoms.csv"
EMBED_MODEL = "models/embedding-001"

def load_documents():
    df = pd.read_csv(CSV_PATH)
    documents = [
        Document(page_content=row["clean_text"], metadata={"label": row["label"]})
        for _, row in df.iterrows()
    ]
    # Split documents into chunks for better retrieval
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

def create_vector_store(embedding):
    docs = load_documents()
    vector_store = FAISS.from_documents(docs, embedding=embedding)
    vector_store.save_local(VECTOR_DB_PATH)
    return vector_store

def load_vector_store(embedding):
    return FAISS.load_local(VECTOR_DB_PATH, embeddings=embedding, allow_dangerous_deserialization=True)
