🧠 Symptom-Disease Retrieval Assistant
An intelligent medical assistant powered by Machine Learning, LangChain, Gemini Pro, FAISS, and Streamlit. This system allows users to:

🔎 Understand symptoms and treatments of various diseases

💬 Ask general health-related questions

🧠 Automatically classify queries into symptom, treatment, or general query

🧬 Retrieve and generate responses using RAG (Retrieval-Augmented Generation)

🚀 Features
✅ Symptom & treatment search using FAISS vector DB
✅ Intent classification with Logistic Regression
✅ Gemini-based LLM responses via LangChain
✅ Context-aware RAG pipeline for relevant answer generation
✅ Streamlit-powered interactive UI

📁 Project Structure
symptom_disease_project/
│
├── app.py                      # 🔷 Streamlit UI entry point
├── query_handler.py           # 🔍 Handles query classification & response
├── query_classifier.py        # 🧠 Trains intent classifier
├── vector_store.py            # 📚 Loads FAISS vector database
├── initializer_vector_db.py   # 🧱 Builds FAISS vector DB from dataset
├── llm_chain.py               # 🤖 LLM & LangChain QA chain setup
│
├── Data/
│   ├── classifier_dataset.csv        # Data for intent classification
│   ├── cleaned_symptoms.csv          # Main dataset for vectorization
│   └── faiss_symptom_index/          # FAISS vector store
│
├── .env                      # 🔐 Contains Gemini API key (excluded from Git)
├── requirements.txt          # 📦 Project dependencies
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
