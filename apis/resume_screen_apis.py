"""Screening the Resumes API"""

from typing import List
from fastapi import APIRouter, UploadFile

from screening.profile_screening import profile_screen_results

router = APIRouter()


@router.post("/screenjd")
async def screen_jd(jd_id: int, bu_id: int, profiles: List[UploadFile]):
    """Screening profiles with JD"""

    results = profile_screen_results(jd_id=jd_id, bu_id=bu_id, resumes=profiles)
    return {"message": "Success", "data": results}


# @router.post("/selectcandidates")
# async def select_candidates(
#     jd_id: int,
#     bu_id: int,
#     profiles: List[UploadFile],
#     selected_candidates: List[Candidate],
# ):
#     """Screening profiles with JD"""

#     results = save_selected_candidates(
#         jd_id=jd_id, bu_id=bu_id, resumes=profiles, candidates=selected_candidates
#     )
#     return {"message": "Success", "data": results}
