# 🏥 Intelligent Medical Chatbot

**A Knowledge Representation & Reasoning Enhanced Conversational AI for Preliminary Symptom Assessment**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [How It Works](#how-it-works)
- [Team Members](#team-members)
- [License](#license)

---

## 🎯 Overview

This project is an AI-powered medical chatbot that combines **Knowledge Representation & Reasoning (KRR)** with **Retrieval-Augmented Generation (RAG)** to provide intelligent, explainable symptom assessment.

Unlike traditional chatbots that simply retrieve information, our system:
- 🧠 **Reasons** about diseases using a formal medical ontology, before the LLM ever sees the query
- 🔍 **Retrieves** relevant medical documents semantically, re-ranked using the reasoning output
- 💡 **Explains** its reasoning process transparently, live, in the UI
- 💬 **Remembers** conversation context for natural follow-ups

**⚠️ Disclaimer:** This is an educational project. It does NOT replace professional medical advice, diagnosis, or treatment.

---

## ✨ Features

### Core Capabilities
- **Medical Ontology**: Formal knowledge base covering 4 diseases (Dengue Fever, Malaria, Common Cold, Migraine), their symptoms, severity, treatments, complications, and 3 inference rules
- **Reasoning Engine**: Rule-based system that applies medical logic to infer conditions and assign confidence scores
- **RAG Integration**: Semantic search over medical text chunks using FAISS + `all-MiniLM-L6-v2` embeddings, re-ranked by KRR-inferred diseases
- **Explainable AI**: A persistent reasoning panel shows extracted symptoms, disease candidates, and confidence scores as the conversation unfolds
- **Context Awareness**: Maintains conversation history for natural follow-up questions ("what causes it?", "what's the treatment?")
- **Urgency Detection**: Flags when a symptom or top disease candidate requires immediate medical attention

### User Interface
- Custom web frontend (HTML/CSS/JS) served independently of the backend
- **Live reasoning ledger** — symptoms, disease confidence bars, and urgency alerts update in real time, always visible (not tucked away in a collapsible panel)
- Intent tag per response (symptom_query / treatment_query / general_query)
- Session-based conversation history with one-click reset

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────┐
│         User Query Input                 │
└──────────────┬────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  1. Intent Classification (ML)            │
└──────────────┬─────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  2. Symptom Extraction (NLP + Ontology)   │
└──────────────┬─────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  3. Disease Reasoning (KRR)               │
│     • Symptom Matching                    │
│     • Rule Application                    │
│     • Confidence Scoring                  │
└──────────────┬─────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  4. Document Retrieval (RAG + FAISS)      │
│     Re-ranked using KRR disease candidates│
└──────────────┬─────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  5. Knowledge Synthesis                   │
│     (Reasoning + Documents + History)     │
└──────────────┬─────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  6. LLM Response (Google Gemini 2.5 Flash)│
└──────────────┬─────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  7. FastAPI Response → Frontend Display   │
│     with live reasoning visualization     │
└──────────────────────────────────────────┘
```

The backend (`main.py`, built with **FastAPI**) exposes the entire pipeline above as a REST API, decoupled from the UI. The frontend (`index.html`) is a standalone client that consumes that API — meaning any interface (web, mobile, another service) could plug into the same reasoning pipeline.

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Step 1: Clone the Repository
```bash
git clone https://github.com/Abdulmoeez1010/Disease-Retrieval-Assistant-using-RAG-.git
cd Disease-Retrieval-Assistant-using-RAG-
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 5: Verify Data Files
Ensure these exist:
- `Data/cleaned_symptoms.csv`
- `Data/faiss_symptom_index/` (folder with FAISS index)
- `query_classifier.joblib`

---

## 💻 Usage

### Running the Application

**1. Start the backend (FastAPI):**
```bash
uvicorn main:app --reload --port 8000
```
This exposes the reasoning + RAG + LLM pipeline at `http://localhost:8000`.

**2. Open the frontend:**
Simply open `index.html` in your browser (double-click, or serve it with any static server). It talks to the backend at `http://localhost:8000`.

### Example Interaction
```
You: I have fever and red spots on my skin

Bot: I understand you're experiencing fever and red spots, which must be
     concerning. Based on my analysis, these symptoms are commonly associated
     with Dengue Fever...

[Live in the reasoning ledger, no click required]
     🧬 Extracted Symptoms: High Fever, Skin Rash
     🔬 Disease Analysis:
       1. Dengue Fever — 80%   (matched: High Fever, Skin Rash, Severe Headache)
       ⚠️ Requires immediate medical attention

You: What causes it?

Bot: Regarding the Dengue Fever we discussed, it's caused by the dengue
     virus, transmitted through the bite of infected Aedes mosquitoes...
```

### Controls
- Type symptoms or questions naturally in the chat input
- Watch the **reasoning ledger** on the left update live — no need to expand anything
- Click **"Clear conversation"** to reset the session

---

## 📁 Project Structure
```
symptom_disease_project/
│
├── main.py                     # FastAPI backend (REST API entry point)
├── index.html                  # Custom frontend (chat + live reasoning ledger)
├── query_handler.py            # Main orchestrator: KRR + RAG + LLM pipeline
├── llm_chain.py                # LLM prompt engineering & chain
├── vector_store.py             # FAISS vector database operations
├── medical_ontology.py         # Medical knowledge representation
├── reasoning_engine.py         # Reasoning logic & inference
├── query_classifier.py         # Intent classifier training script
├── query_classifier.joblib     # Trained intent classifier
├── debug_test.py               # Standalone script to test API key / LLM connectivity
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not committed)
├── README.md                   # This file
│
└── Data/
    ├── cleaned_symptoms.csv    # Medical text dataset
    ├── classifier_dataset.csv  # Intent classifier training data
    └── faiss_symptom_index/    # FAISS vector index
        ├── index.faiss
        └── index.pkl
```

---

## 🛠️ Technologies Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.9+ | Core programming |
| **Backend API** | FastAPI + Uvicorn | REST API serving the reasoning pipeline |
| **Frontend** | HTML / CSS / JavaScript | Chat interface with live reasoning visualization |
| **LLM** | Google Gemini 2.5 Flash | Natural language generation |
| **RAG Framework** | LangChain | Orchestration & prompting |
| **Vector DB** | FAISS | Semantic search |
| **Embeddings** | HuggingFace (`all-MiniLM-L6-v2`) | Text vectorization |
| **ML** | Scikit-learn (TF-IDF + Logistic Regression) | Intent classification |
| **Data Processing** | Pandas, NumPy | Data manipulation |

---

## 🧠 How It Works

### 1. Medical Ontology (Knowledge Representation)
```python
"dengue_fever": {
    "name": "Dengue Fever",
    "symptoms": ["high_fever", "severe_headache", "pain_behind_eyes",
                 "joint_pain", "skin_rash"],
    "severity": "moderate_to_severe",
    "requires_immediate_care": True,
    "treatments": ["rest", "hydration", "pain_relievers"]
}
```
The ontology currently defines **4 diseases** (Dengue Fever, Malaria, Common Cold, Migraine) with their symptoms, severity, causes, treatments, complications, and diagnosis methods — structured as a Python knowledge base rather than free text.

### 2. Reasoning Rules
```python
IF high_fever AND severe_headache
   AND (skin_rash OR pain_behind_eyes OR joint_pain)
THEN dengue_fever (confidence: 0.80)
```
Symptom-to-disease matching produces a base confidence score (matched symptoms ÷ total symptoms for that disease); explicit rules can then boost or add to that score.

### 3. RAG Pipeline
- User query → embed query (`all-MiniLM-L6-v2`) → search FAISS index → retrieve top-k chunks
- Retrieval is re-ranked using the diseases the KRR layer inferred, so results align with the reasoning rather than raw semantic similarity alone
- The KRR's structured findings are prepended to the retrieved documents before being handed to the LLM — the model answers with reasoning as grounding, not just retrieved text

### 4. Explainable Output
- Extracted symptoms, disease candidates with confidence scores, matched symptoms, and urgency flags are all surfaced live in the frontend — not hidden, not post-hoc

---

## 👥 Team Members

- **[Student 1 Name]** - [Roll Number] - Ontology Design & Reasoning Engine
- **[Student 2 Name]** - [Roll Number] - RAG Implementation & Vector Store
- **[Student 3 Name]** - [Roll Number] - LLM Integration & Prompting
- **[Student 4 Name]** - [Roll Number] - Backend & Frontend Development

**Supervisor:** [Professor Name]
**Course:** Knowledge Representation & Reasoning
**Institution:** Air University, Islamabad
**Semester:** [Fill in]

---

## 🔮 Future Enhancements

- [ ] Expand ontology beyond the current 4 diseases
- [ ] Multi-language support (Urdu, Arabic, etc.)
- [ ] Temporal reasoning for symptom progression tracking
- [ ] Bayesian or ML-based confidence scoring instead of simple ratio matching
- [ ] Voice input/output
- [ ] Migrate ontology to a formal standard (OWL / SNOMED-CT) for large-scale reasoning

---

## 🤝 Contributing

This is an academic project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**IMPORTANT:** This chatbot is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

- Always seek the advice of your physician or qualified health provider
- Never disregard professional medical advice because of something you read here
- If you have a medical emergency, call your local emergency number immediately
- This system should be used as a supplement to, not a replacement for, healthcare services

---

**Made by Abdul Moeez**

*Last Updated: July 2026*
