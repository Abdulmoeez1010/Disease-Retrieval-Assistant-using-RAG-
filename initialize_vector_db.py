# initialize_vector_db.py
from vector_store import create_vector_store
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("📦 Creating FAISS vector DB from symptoms CSV...")
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    create_vector_store(embedding)
    print("✅ Vector store created at 'data/faiss_symptom_index/'")

if __name__ == "__main__":
    main()
