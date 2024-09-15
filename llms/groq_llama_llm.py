"""Loading LLM"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def load_llm():
    """LLM Model to be used"""
    llm = ChatGroq(
        model="llama3-70b-8192",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.8,
    )
    return llm
