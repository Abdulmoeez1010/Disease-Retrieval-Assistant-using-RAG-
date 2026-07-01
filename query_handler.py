"""
KRR-Enhanced Query Handler
Combines Knowledge Representation, Reasoning, and RAG
"""

import os
import joblib
import time
from dotenv import load_dotenv

from vector_store import load_vector_store
from llm_chain import get_qa_chain
from medical_ontology import MedicalOntology
from reasoning_engine import MedicalReasoningEngine

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI


# -------------------- ENV SETUP --------------------
load_dotenv()
gem_api = os.getenv("GEMINI_API_KEY")


# -------------------- LOAD LLM --------------------
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    temperature=0.5,
    google_api_key=gem_api
)


# -------------------- LOAD EMBEDDINGS --------------------
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


# -------------------- LOAD VECTOR STORE --------------------
vector_store = load_vector_store(embeddings)


# -------------------- LOAD INTENT CLASSIFIER --------------------
classifier = joblib.load("query_classifier.joblib")


# -------------------- INITIALIZE KRR COMPONENTS --------------------
ontology = MedicalOntology()
reasoning_engine = MedicalReasoningEngine(ontology)


# -------------------- INTENT CLASSIFICATION --------------------
def classify_query(query: str) -> str:
    """Predict user intent"""
    return classifier.predict([query])[0]


# -------------------- DETECT FOLLOW-UP QUESTIONS --------------------
def is_followup_question(query: str) -> bool:
    """Detect if query is a follow-up"""
    followup_indicators = [
        'it', 'that', 'this', 'those', 'these',
        'what about', 'tell me more', 'why', 'how',
        'what causes', 'what treatment'
    ]
    query_lower = query.lower()
    
    if len(query.split()) < 8:
        return any(indicator in query_lower for indicator in followup_indicators)
    return False


# -------------------- BUILD CONTEXTUAL QUERY --------------------
def build_contextual_query(query: str, chat_history: list) -> str:
    """Build query with conversation context"""
    if is_followup_question(query) and chat_history:
        recent_context = []
        for turn in chat_history[-6:]:
            if turn["role"] == "user":
                recent_context.append(turn["content"])
        
        if recent_context:
            context_text = " | ".join(recent_context)
            return f"{context_text} | {query}"
    
    symptoms_context = []
    for turn in chat_history[-4:]:
        if turn["role"] == "user":
            symptoms_context.append(turn["content"])
    
    if symptoms_context:
        context_text = " | ".join(symptoms_context[-2:])
        return f"{context_text} | {query}"
    
    return query


# -------------------- ENHANCED RETRIEVAL WITH KRR --------------------
def retrieve_relevant_docs(query: str, chat_history: list, inferred_diseases: list, k: int = 8):
    """
    KRR-enhanced retrieval: Use inferred diseases to improve document retrieval
    """
    contextual_query = build_contextual_query(query, chat_history)
    
    # If we have disease inferences, add them to query for better retrieval
    if inferred_diseases:
        top_diseases = [d["disease_name"] for d in inferred_diseases[:2]]
        disease_context = " | ".join(top_diseases)
        contextual_query = f"{contextual_query} | {disease_context}"
    
    docs = vector_store.similarity_search(contextual_query, k=k*2)
    
    # Re-rank based on disease relevance
    if inferred_diseases and docs:
        disease_terms = set()
        for disease in inferred_diseases[:3]:
            disease_terms.add(disease["disease_id"].replace("_", " "))
            disease_terms.add(disease["disease_name"].lower())
        
        scored_docs = []
        for doc in docs:
            content_lower = doc.page_content.lower()
            score = sum(1 for term in disease_terms if term in content_lower)
            scored_docs.append((score, doc))
        
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in scored_docs[:k]]
    
    return docs[:k]


# -------------------- MAIN KRR QUERY HANDLER --------------------
def handle_query(query: str, chat_history: list, max_retries: int = 2):
    """
    KRR-Enhanced RAG Pipeline:
    1. Intent classification
    2. Symptom extraction (KRR)
    3. Disease reasoning (KRR)
    4. Document retrieval (RAG)
    5. LLM synthesis (with KRR + RAG context)
    """
    intent = classify_query(query)
    print(f"🔍 Detected intent: {intent}")

    # ========== STEP 1: EXTRACT SYMPTOMS (KRR) ==========
    extracted_symptoms = reasoning_engine.extract_symptoms_from_text(query)
    
    # Also extract from recent history
    for turn in chat_history[-3:]:
        if turn["role"] == "user":
            hist_symptoms = reasoning_engine.extract_symptoms_from_text(turn["content"])
            extracted_symptoms.extend(hist_symptoms)
    
    extracted_symptoms = list(set(extracted_symptoms))  # Remove duplicates
    
    if extracted_symptoms:
        print(f"🧬 Extracted symptoms: {extracted_symptoms}")
    
    # ========== STEP 2: REASON ABOUT DISEASES (KRR) ==========
    disease_candidates = []
    reasoning_explanation = ""
    
    if extracted_symptoms and intent in ["symptom_query", "treatment_query"]:
        disease_candidates = reasoning_engine.reason_about_diseases(extracted_symptoms)
        
        if disease_candidates:
            print(f"🧠 Reasoning found {len(disease_candidates)} disease candidates:")
            for i, disease in enumerate(disease_candidates[:3]):
                print(f"   {i+1}. {disease['disease_name']} (confidence: {disease['confidence']*100:.0f}%)")
            
            # Generate reasoning explanation
            reasoning_explanation = reasoning_engine.explain_reasoning(
                extracted_symptoms,
                disease_candidates
            )
            
            # Check urgency
            urgency = reasoning_engine.check_urgency(extracted_symptoms, disease_candidates)
            if urgency["is_urgent"]:
                print(f"⚠️  URGENT: {urgency['reasons'][0]}")
    
    # ========== STEP 3: RETRIEVE DOCUMENTS (RAG) ==========
    docs = []
    if intent in ["symptom_query", "treatment_query"]:
        docs = retrieve_relevant_docs(query, chat_history, disease_candidates, k=8)
        print(f"📄 Retrieved {len(docs)} documents")
    
    # ========== STEP 4: PREPARE STRUCTURED KNOWLEDGE FOR LLM ==========
    structured_knowledge = ""
    
    if disease_candidates:
        structured_knowledge = "\n\n--- REASONING ENGINE ANALYSIS ---\n"
        structured_knowledge += reasoning_explanation + "\n"
        
        # Add detailed info about top candidate
        top_disease = disease_candidates[0]
        disease_info = ontology.get_disease_info(top_disease["disease_id"])
        
        if disease_info:
            structured_knowledge += f"\n**Detailed Information about {top_disease['disease_name']}:**\n"
            structured_knowledge += f"- Severity: {disease_info.get('severity', 'Unknown')}\n"
            structured_knowledge += f"- Typical Symptoms: {', '.join(disease_info.get('symptoms', []))}\n"
            structured_knowledge += f"- Treatments: {', '.join(disease_info.get('treatments', []))}\n"
            
            if disease_info.get("requires_immediate_care"):
                structured_knowledge += f"- ⚠️ **Requires immediate medical attention**\n"
    
    # ========== STEP 5: COMBINE STRUCTURED KNOWLEDGE WITH RETRIEVED DOCS ==========
    if structured_knowledge:
        # Insert structured knowledge before documents
        if docs:
            from langchain_core.documents import Document
            structured_doc = Document(
                page_content=structured_knowledge,
                metadata={"source": "reasoning_engine"}
            )
            docs = [structured_doc] + docs
    
    # ========== STEP 6: GET LLM RESPONSE ==========
    chain = get_qa_chain(llm)
    
    for attempt in range(max_retries):
        try:
            if docs:
                result = chain.invoke({
                    "documents": docs,
                    "question": query,
                    "chat_history": chat_history
                })
            else:
                result = chain.invoke({
                    "documents": [],
                    "question": query,
                    "chat_history": chat_history
                })

            # Prepare KRR data for UI display
            krr_data = {
                "symptoms": extracted_symptoms,
                "diseases": disease_candidates[:3] if disease_candidates else [],
                "reasoning_explanation": reasoning_explanation if reasoning_explanation else None,
                "urgency": reasoning_engine.check_urgency(extracted_symptoms, disease_candidates) if extracted_symptoms else {},
                "doc_count": len(docs)
            }

            return intent, result, krr_data

        except Exception as e:
            error_msg = str(e)
            
            if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)
                    print(f"⏳ Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    return intent, "⚠️ API rate limit exceeded. Please try again shortly.", {}
            else:
                print(f"❌ Error: {error_msg}")
                return intent, f"❌ Error: {error_msg}", {}

    return intent, "❌ Failed after retries. Please try again.", {}


# -------------------- SESSION MANAGEMENT --------------------
class ChatSession:
    """Manages conversation history"""
    def __init__(self, max_history: int = 10):
        self.history = []
        self.max_history = max_history
    
    def add_message(self, role: str, content: str):
        """Add message to history"""
        self.history.append({"role": role, "content": content})
        
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_history(self):
        """Get conversation history"""
        return self.history
    
    def clear(self):
        """Clear conversation history"""
        self.history = []