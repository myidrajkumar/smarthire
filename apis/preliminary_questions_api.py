"""Questions Generation"""

from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from preliminary_round.preliminary_handling import (
    generate_credentials_and_send_email,
    generate_interview_questions,
    get_interview_questions,
    get_jd_doc,
    save_questions,
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")
attending_candidates = {}


class FirstRound(BaseModel):
    """Request Parameters"""

    jd_id: int
    bu_id: int
    candidate_list: List[int]


@router.post("/sendpreliminaryquestions")
async def send_preliminary_questions(request: FirstRound):
    """Generate Questions"""

    jd_id, bu_id, candidate_list = request.jd_id, request.bu_id, request.candidate_list
    jd_txt = get_jd_doc(request.jd_id, request.bu_id)
    response = generate_interview_questions(jd_txt, len(candidate_list))
    save_questions(response, candidate_list, jd_id, bu_id)

    generate_credentials_and_send_email(candidate_list, jd_id, bu_id)
    return {"message": "Success"}


@router.post("/startexam/{candidateid}")
async def start_exam(candidateid: str):
    """Start the exam and set a 1-hour timer"""
    attending_candidates.update({candidateid: datetime.now(timezone.utc)})
    return {"message": "Exam started, you have 1 hour to complete it"}


@router.get("/triggerexam", response_class=HTMLResponse)
async def show_exam(request: Request, jd_id: int, bu_id: int, candidate_id: int):
    """Displaying Questions"""
    assigned_questions = get_interview_questions(jd_id, bu_id, candidate_id)
    return templates.TemplateResponse(
        "exam.html", {"request": request, "questions": assigned_questions}
    )
