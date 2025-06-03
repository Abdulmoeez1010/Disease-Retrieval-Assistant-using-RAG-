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

🛠️ How to Run the Project
Follow these steps to set up and run the application locally:
1. 📦 Extract the Project
Unzip the project folder and navigate to it in your terminal:
cd symptom_disease_project

2. 🔃 Create and Activate Virtual Environment
Create a virtual environment:
python -m venv venv

Activate the virtual environment:
Windows:
venv\Scripts\activate

3. 📥 Install Requirements
pip install -r requirements.txt

4. 🔐 Add Gemini API Key (I'm not sure about this step)
Create a .env file in the root directory and add your key:
GEMINI_API_KEY=your_google_gemini_api_key

5. 🧱 (Optional) Rebuild FAISS Vector DB (if needed)
If you want to rebuild the FAISS index:
python initializer_vector_db.py

6. 🚀 Launch the App
Run the Streamlit UI:
streamlit run app.py


📈 Example Queries
"What are the symptoms of diabetes?"

"How can asthma be treated?"

"Tell me about the cause of migraine"

"What is COVID-19?"

"How to treat sore throat naturally?"

🧠 Tech Stack
LangChain – Query handling, prompt engineering, RAG

Google Gemini (via LangChain) – LLM responses

FAISS – Vector similarity search on symptom documents

Scikit-learn (Logistic Regression) – Query intent classification

Streamlit – Frontend for user interaction

Python – Core development language

📚 License
This project is built as part of an academic course and is open for educational use.

