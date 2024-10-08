"""Questions Generation"""

from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from db.connect import save_candidate_score_with_status
from preliminary_round.preliminary_handling import (
    generate_credentials_and_send_email,
    generate_interview_questions,
    get_answers,
    get_interview_questions,
    get_jd_doc,
    save_questions,
    update_candidate_preliminart_interview_status,
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
    update_candidate_preliminart_interview_status(jd_id, bu_id, candidate_list)
    return {"message": "Success"}


@router.post("/startexam/{candidateid}")
async def start_exam(candidateid: int):
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


class Submission(BaseModel):
    """Canidate Answers"""

    bu_id: int
    jd_id: int
    candidate_id: int
    answers: List[str]


@router.post("/submitanswers")
async def submit_answers(submission: Submission):
    """Evaluating answers"""
    start_time = datetime.now(timezone.utc) - timedelta(
        minutes=60
    )  # Example start time for demo purposes
    current_time = datetime.now(timezone.utc)

    candidate_id, jd_id, bu_id = (
        submission.candidate_id,
        submission.jd_id,
        submission.bu_id,
    )

    # Calculate time difference
    time_difference = current_time - start_time
    attending_candidates.pop(candidate_id)

    if time_difference > timedelta(hours=1):
        raise HTTPException(
            status_code=400, detail="Time is up! You cannot submit after 1 hour."
        )

    correct_answers = get_answers(candidate_id, jd_id, bu_id)
    score = sum(
        1 for i, answer in enumerate(submission.answers) if answer == correct_answers[i]
    )

    # Store the result in the database
    save_candidate_score_with_status(
        candidate_id, f"{score}/{len(correct_answers)}", "Preliminary: Attended"
    )

    return {"score": score, "out_of": len(correct_answers)}
