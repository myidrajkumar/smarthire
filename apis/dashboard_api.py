"""Dashboard APIs"""

from fastapi import APIRouter

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


router = APIRouter()


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
    return {"message": "Success", "data": data}


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
    return {"message": "Success", "data": data}


@router.get("/api/jobs")
def get_jobs():
    """Getting Jobs"""

    data = get_jobs_from_db()
    return {"message": "Success", "data": data}
