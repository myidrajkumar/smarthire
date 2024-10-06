"""Questions Generation"""

from datetime import datetime, timezone
import time
from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.connect import get_jd_from_db, save_question_answers_to_db
from preliminary_round.preliminary_handling import get_interview_questions
from utils.file_utils import save_files_temporarily_and_get_delete

router = APIRouter()

templates = Jinja2Templates(directory="templates")

attending_candidates = {}


@router.get("/generatequestions")
async def generate_questions(jd_id: int, bu_id: int, candidate_id: int):
    """Generate Questions"""

    db_result = get_jd_from_db(jd_id, bu_id)
    jd_txt = save_files_temporarily_and_get_delete(
        db_result.get("title"), db_result.get("doc")
    )

    response = get_interview_questions(jd_txt)

    save_questions(response, candidate_id, jd_id, bu_id)
    return {"message": "Success", "data": response}


@router.post("/startexam/{candidateid}")
async def start_exam(candidateid: str, background_tasks: BackgroundTasks):
    """Start the exam and set a 1-hour timer"""
    background_tasks.add_task(exam_timer)
    attending_candidates.update({candidateid: datetime.now(timezone.utc)})
    return {"message": "Exam started, you have 1 hour to complete it"}


@router.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    """Serving HTML"""
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )


async def exam_timer():
    """Timer to exam"""
    time.sleep(3600)
    print("Time's up!")


def save_questions(response, candidate_id, jd_id, bu_id):
    """Save Questions"""

    save_question_answers_to_db(candidate_id, jd_id, bu_id, response)
