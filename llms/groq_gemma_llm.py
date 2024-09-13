"""Loading LLM"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def load_llm():
    """LLM Model to be used"""
    llm = ChatGroq(
        model="gemma2-9b-it",
        api_key=os.getenv("GROQ_API_KEY"),
    )
    return llm
