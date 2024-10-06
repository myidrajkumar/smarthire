"""Questions Generation"""

from datetime import datetime, timezone
import time
from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from preliminary_round.preliminary_handling import (
    generate_interview_questions,
    get_interview_questions,
    get_jd_doc,
    save_questions,
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")
attending_candidates = {}


@router.get("/generatequestions")
async def generate_questions(jd_id: int, bu_id: int, candidate_id: int):
    """Generate Questions"""

    jd_txt = get_jd_doc(jd_id, bu_id)
    response = generate_interview_questions(jd_txt)

    save_questions(response, candidate_id, jd_id, bu_id)
    return {"message": "Success", "data": response}


@router.post("/startexam/{candidateid}")
async def start_exam(candidateid: str, background_tasks: BackgroundTasks):
    """Start the exam and set a 1-hour timer"""
    background_tasks.add_task(exam_timer)
    attending_candidates.update({candidateid: datetime.now(timezone.utc)})
    return {"message": "Exam started, you have 1 hour to complete it"}


@router.get("/triggerexam", response_class=HTMLResponse)
async def show_exam(request: Request, jd_id: int, bu_id: int, candidate_id: int):
    """Displaying Questions"""
    assigned_questions = get_interview_questions(jd_id, bu_id, candidate_id)
    return templates.TemplateResponse(
        "exam.html", {"request": request, "questions": assigned_questions}
    )


async def exam_timer():
    """Timer to exam"""
    time.sleep(3600)
    print("Time's up!")
