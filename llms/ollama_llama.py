"""Loading LLM"""

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()


def load_llm():
    """LLM Model to be used"""
    llm = ChatOllama(
        model="llama3.1:latest",
        temperature=0.5,
    )
    return llm
