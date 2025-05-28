import os
import joblib
from dotenv import load_dotenv

from vector_store import load_vector_store
from llm_chain import get_qa_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Load .env variables
load_dotenv()
gem_api = os.getenv("GEMINI_API_KEY")

# Load LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    google_api_key=gem_api
)

# Load Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=gem_api
)

# Load FAISS vector store using embeddings
vector_store = load_vector_store(embeddings)

# Load trained intent classifier
classifier = joblib.load("query_classifier.joblib")


def classify_query(query: str) -> str:
    """Predict user intent (symptom_query, treatment_query, etc.)"""
    return classifier.predict([query])[0]


def handle_query(query: str) -> str:
    """Route query based on intent and return answer"""
    intent = classify_query(query)
    print(f"🔍 Detected intent: {intent}")

    # Prepare docs (retrieval) only if intent needs it
    docs = []
    if intent in ["symptom_query", "treatment_query"]:
        docs = vector_store.similarity_search(query, k=10)

    # Get QA chain using current LLM
    chain = get_qa_chain(llm)

    # Run the chain
    result = chain(
        {"input_documents": docs, "question": query},
        return_only_outputs=True
    )
    return intent, result["output_text"]


