"""Dashboard APIs"""

from fastapi import APIRouter
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from db.connect import (
    get_candidate_experience_from_db,
    get_compliance_metrics_from_db,
    get_diversity_metrics_from_db,
    get_job_analytics_from_db,
    get_jobs_from_db,
    get_kpis_from_db,
    get_offer_hiring_analytics_from_db,
    get_recruitment_efficiency_from_db,
    get_screening_interview_analytics_from_db,
    get_sourcing_analytics_from_db,
)
from llms.groq_llama_llm_versatile import load_llm

router = APIRouter()
llm = load_llm()


@router.get("/analytics/kpis")
def get_kpis():
    """Getting KPIs"""

    data = get_kpis_from_db()
    return {"message": "Success", "data": data}


@router.get("/analytics/jobs/{job_id}")
def get_job_analytics(job_id: int):
    """Getting job specific information"""

    data = get_job_analytics_from_db(job_id)
    return {"message": "Success", "data": data}


@router.get("/analytics/sourcing")
def get_sourcing_analytics():
    """Getting source analytics"""

    data = get_sourcing_analytics_from_db()

    message = """Sourcing data: {data}. This contains 'source_breakdown', 'geographical_sourcing'
    and 'cost_per_source'. Please provide a brief summary of 'source_breakdown'and 'cost_per_source'.
    DO NOT CONSIDER 'geographical_sourcing' data at all.
    Please just provide summary in just 2 lines. Please provide in JSON format with the following fields

    * source_breakdown_summary - 2 lines paragraph summary. This content should be in MD or markdown format
    * cost_per_source_summary - 2 lines paragraph summary. This content should be in MD or markdown format
    """

    parser = PydanticOutputParser(pydantic_object=SourcingSummary)
    summary = get_summary_from_llm(message, data, parser)
    return {"message": "Success", "info": summary, "data": data}


@router.get("/analytics/screeninginterview")
def get_screening_interview_analytics():
    """Get screening statistics"""

    data = get_screening_interview_analytics_from_db()
    return {"message": "Success", "data": data}


@router.get("/analytics/offers")
def get_offer_hiring_analytics():
    """Getting offere analytics"""

    data = get_offer_hiring_analytics_from_db()
    return {"message": "Success", "data": data}


@router.get("/analytics/diversity")
def get_diversity_metrics():
    """Getting Diversity Metrics"""

    data = get_diversity_metrics_from_db()
    return {"message": "Success", "data": data}


@router.get("/analytics/candidateexperience")
def get_candidate_experience():
    """Candidates Experience"""

    data = get_candidate_experience_from_db()
    return {"message": "Success", "data": data}


@router.get("/analytics/efficiency")
def get_recruitment_efficiency():
    """Recruitment Efficiency"""

    data = get_recruitment_efficiency_from_db()
    return {"message": "Success", "data": data}


@router.get("/analytics/compliance")
def get_compliance_metrics():
    """Get the compliance metrics"""

    data = get_compliance_metrics_from_db()

    message = """Compliance data: {data}. This contains 'gender_distribution', 'ethnicity_distribution'
    and 'gdpr_compliance_rate'. Please provide insights and suggestions with 4 lines of pargraph summary.
    This content should be in MD or Markdown format"""

    parser = StrOutputParser()

    summary = get_summary_from_llm(message, data, parser)

    return {"message": "Success", "info": summary, "data": data}


@router.get("/api/jobs")
def get_jobs():
    """Getting Jobs"""

    data = get_jobs_from_db()
    return {"message": "Success", "data": data}


class SourcingSummary(BaseModel):
    """Sourcing Summary Model"""

    source_breakdown_summary: str
    cost_per_source_summary: str


def get_summary_from_llm(message, data, parser):
    """Getting Summary from GenAI"""
    prompt_template = ChatPromptTemplate(
        [
            (
                "user",
                message,
            ),
        ]
    )

    chain = prompt_template | llm | parser
    return chain.invoke({"data": data})
