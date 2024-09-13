"""Loading LLM"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def load_llm():
    """LLM Model to be used"""
    llm = ChatGroq(model="mixtral-8x7b-32768")
    return llm
