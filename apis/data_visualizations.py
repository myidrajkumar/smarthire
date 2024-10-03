"""To plot charts"""

import pandas as pd
import plotly.express as px
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from transformers import pipeline
from langchain_core.prompts import ChatPromptTemplate

from llms.ollama_llama import load_llm

router = APIRouter()


def get_candidate_data():
    """Candidate Data"""
    data = {
        "Stage": ["Applied", "Screening", "Interview", "Offer Sent", "Hired"],
        "Number of Candidates": [120, 80, 50, 20, 10],
    }
    return pd.DataFrame(data)


def generate_chart():
    """Generating Chart"""
    df = get_candidate_data()
    fig = px.bar(
        df,
        x="Stage",
        y="Number of Candidates",
        title="Candidates at Different Stages",
        labels={"Stage": "Recruitment Stage", "Number of Candidates": "Candidates"},
    )

    return fig.to_html(full_html=False)


@router.get("/recruitmentchart", response_class=HTMLResponse)
def recruitment_chart():
    """Recruitment Chart"""
    chart_html = generate_chart()
    return HTMLResponse(content=chart_html)


nlp = pipeline("text-generation", model="gpt-2")


def interpret_query(user_input):
    """Get User Input"""
    # Example: Process the query to infer user intent (e.g., "Show candidate distribution")
    response = nlp(user_input, max_length=50, num_return_sequences=1)
    return response[0]["generated_text"]


@router.get("/dynamicchart", response_class=HTMLResponse)
def dynamic_chart(query: str):
    """Dynamic Chart"""

    llm = load_llm()

    prompt_template = ChatPromptTemplate(
        [
            (
                "user",
                query,
            ),
        ]
    )

    chain = prompt_template | llm
    interpreted_text = interpret_query(query)

    # For simplicity, generate the same chart for now.
    # Later, this can generate different charts based on `interpreted_text`.
    chart_html = generate_chart()

    # Return both the interpreted text and the chart
    html_content = f"<h3>Query Interpretation: {interpreted_text}</h3>" + chart_html
    return HTMLResponse(content=html_content)
