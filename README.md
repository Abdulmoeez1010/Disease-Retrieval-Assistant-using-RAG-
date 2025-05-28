# 🧠 Symptom-Disease Retrieval Assistant

An intelligent medical assistant built using **LangChain**, **FAISS**, **Streamlit**, and **Machine Learning**, which helps users:
- Understand **symptoms and treatments** of diseases
- Ask **general health queries**
- Automatically detect **user intent** (symptom, treatment, general query)
- Retrieve and generate responses using LLMs + RAG (Retrieval-Augmented Generation)

---

## 🚀 Features

- ✅ Symptom & treatment search using **FAISS vector DB**
- ✅ Intent classification with **Logistic Regression**
- ✅ **Query-based document retrieval** using LangChain
- ✅ Gemini-based LLM responses
- ✅ Streamlit UI for smooth interaction

---

## 📁 Project Structure

```bash
symptom_disease_project/
│
├── app.py                      # 🔷 Streamlit UI entry point
├── query_handler.py           # 🔍 Query processing & intent handling
├── query_classifier.py        # 🧠 Classifier training
├── vector_store.py            # 📚 FAISS DB loading
├── llm_chain.py               # 🤖 LangChain prompt and QA chain
├── initializer_vector_db.py   # 🧱 Build vector DB from CSV
│
├── Data/
│   ├── classifier_dataset.csv         # Classifier training data
│   ├── cleaned_symptoms.csv           # Main corpus
│   ├── faiss_symptom_index/           # FAISS vector store
│
├── venv/                     # 🔒 Virtual environment (excluded)
├── .env                      # 🔐 API keys (excluded)
├── .gitignore
└── README.md
