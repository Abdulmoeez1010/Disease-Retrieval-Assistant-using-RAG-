from langchain_huggingface import HuggingFaceEmbeddings
from vector_store import create_vector_store
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("📦 Creating FAISS vector DB...")

    embedding = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    create_vector_store(embedding)
    print("✅ Vector store created successfully.")

if __name__ == "__main__":
    main()