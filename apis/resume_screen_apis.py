"""Screening the Resumes API"""

from typing import List
from fastapi import APIRouter, UploadFile

from screening.profile_screening import (
    get_selected_candidates,
    profile_screen_results,
    save_selected_candidates,
)

router = APIRouter()


@router.post("/screenjd")
async def screen_jd(jd_id: int, bu_id: int, profiles: List[UploadFile]):
    """Screening profiles with JD"""

    results = profile_screen_results(jd_id=jd_id, bu_id=bu_id, resumes=profiles)
    return {"message": "Success", "data": results}


@router.post("/selectcandidates")
async def select_candidates(
    jd_id: int,
    bu_id: int,
    candidate_ids: List[int],
):
    """Selected candidates"""

    save_selected_candidates(jd_id=jd_id, bu_id=bu_id, candidate_ids=candidate_ids)

    return {"message": "Success"}


@router.get("/screenedcandidates")
async def screened_candidates(
    jd_id: int,
    bu_id: int,
):
    """Selected candidates"""

    results = get_selected_candidates(jd_id=jd_id, bu_id=bu_id)

    return {"message": "Success", "data": results}
