"""Questions Generation"""

from fastapi import APIRouter

from db.connect import get_jd_from_db, save_question_answers_to_db
from preliminary_round.preliminary_handling import get_interview_questions
from utils.file_utils import save_files_temporarily_and_get_delete

router = APIRouter()


@router.get("/generatequestions")
async def generate_questions(jd_id: int, bu_id: int, candidate_id: int):
    """Generate Questions"""

    db_result = get_jd_from_db(jd_id, bu_id)
    jd_txt = save_files_temporarily_and_get_delete(
        db_result.get("title"), db_result.get("doc")
    )

    response = get_interview_questions(jd_txt)

    save_questions(response, candidate_id, jd_id, bu_id)
    questions_set = {
        "job_title": response.job_title,
        "time_limit": response.time_limit,
        "instructions": response.instructions,
        "questions_set": [
            {k: v for k, v in vars(questions).items() if k != "correct_answer"}
            for questions in response.questions_set
        ],
    }

    return {"message": "Success", "data": questions_set}


def save_questions(response, candidate_id, jd_id, bu_id):
    """Save Questions"""
    correct_answer_list = "#END#".join(
        [
            f"{idx}:{question.correct_answer}"
            for idx, question in enumerate(response.questions_set)
        ]
    )
    save_question_answers_to_db(candidate_id, jd_id, bu_id, correct_answer_list)
