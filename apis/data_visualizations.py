"""To plot charts"""

import pandas as pd
import plotly.express as px
from fastapi import APIRouter
from fastapi.responses import HTMLResponse


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


def get_chart_generation_sytem_propmt_msg():
    """Instruct the system to follow this"""
    return """
            You are an AI assistant specialized in generating and
            accurate job descriptions. Your task is to generate a 1 page
            job description that includes

            * Job Title - No creativeness
            * Description - A clear and engaging overview of the job role
            * Responsibilities - A detailed list of duties and responsibilities associated with the role. Please provide in list format
            * Skills & Experience - An in-depth section outlining the required skills and experience with as much detail as possible. This should be in list format only

            Guidelines
            * The job description is as accurate and precise as possible.
            * The experience and skills sections are detailed and tailored to the job title.
            * The language is professional and suitable for a formal job posting.
            * Provide the response in JSON format only
            * Use professional and inclusive language suitable for a formal job posting.
            * Except description, all other fields should be list only


            The Json field names should be the following only
            * JobTitle
            * Description
            * Responsibilities
            * SkillsAndExperience

            The final output should be a well-structured, one-page document ready for publication in job listings.
           """
