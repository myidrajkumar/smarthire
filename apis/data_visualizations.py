"""To plot charts"""

from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, StreamingResponse
from transformers import pipeline
from langchain_core.prompts import ChatPromptTemplate

from db.connect import get_candidates_pipeline, get_time_to_hire
from llms.ollama_llama import load_llm

router = APIRouter()


@router.get("/pipelinechart")
def get_candidates_pipeline_chart():
    """Pipeline Plots"""

    pipeline_data = get_candidates_pipeline()

    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x="stage", y="candidates", data=pipeline_data)
    plt.title("Candidate Pipeline by Stage")

    # Save to BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")


@router.get("/timetohire")
def get_time_to_hire_chart():
    """Time to Hire Charts"""

    time_to_hire_data = get_time_to_hire()

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        x=time_to_hire_data["job_id"].astype(str),  # Treat Job IDs as categorical
        y=time_to_hire_data["avg_time_to_hire"],
    )
    plt.title("Time to Hire Trends by Job ID")
    plt.xlabel("Job IDs")
    plt.ylabel("Average Time to Hire (Days)")

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")


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
