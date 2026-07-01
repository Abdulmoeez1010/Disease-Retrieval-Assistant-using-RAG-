import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_DB_PATH = "data/faiss_symptom_index"
CSV_PATH = "data/cleaned_symptoms.csv"

def load_documents():
    df = pd.read_csv(CSV_PATH)
    documents = [
        Document(
            page_content=row["clean_text"],
            metadata={"label": row["label"]}
        )
        for _, row in df.iterrows()
    ]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )
    return splitter.split_documents(documents)


def create_vector_store(embedding):
    docs = load_documents()
    vector_store = FAISS.from_documents(docs, embedding=embedding)
    vector_store.save_local(VECTOR_DB_PATH)
    return vector_store


def load_vector_store(embedding):
    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings=embedding,
        allow_dangerous_deserialization=True
    )