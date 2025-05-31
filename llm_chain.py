from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.5,
        max_output_tokens = 1000,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

def get_qa_chain(llm):
    template = """You are a medical assistant.

Given the context below, answer the question briefly and helpfully. If the query is about symptoms, include relevant matching symptoms.

CONTEXT: {context}

QUESTION: {question}

ANSWER:"""
    prompt = PromptTemplate(input_variables=["context", "question"], template=template)
    return load_qa_chain(llm, chain_type="stuff", prompt=prompt)
