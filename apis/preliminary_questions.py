"""Questions Generation"""

from typing import List
from fastapi import APIRouter
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from db.connect import get_jd_from_db, save_question_answers_to_db
from llms.googlegenai_llm import load_llm
from utils.file_utils import save_files_temporarily_and_get_delete

router = APIRouter()


class Question(BaseModel):
    """Questions"""

    question: str
    options: List[str]
    correct_answer: str


class QuestionsSet(BaseModel):
    """Questions Set"""

    job_title: str
    time_limit: str
    instructions: str
    questions_set: list[Question]


@router.get("/generatequestions")
async def generate_questions(jd_id: int, bu_id: int, candidate_id: int):
    """Generate Questions"""

    db_result = get_jd_from_db(jd_id, bu_id)
    jd_txt = save_files_temporarily_and_get_delete(
        db_result.get("title"), db_result.get("doc")
    )

    llm = load_llm()

    prompt_template = ChatPromptTemplate(
        [
            (
                "system",
                get_interview_questions_sytem_propmt_msg(),
            ),
            (
                "user",
                get_interview_questions_user_propmt_msg(),
            ),
        ]
    )

    parser = PydanticOutputParser(pydantic_object=QuestionsSet)
    chain = prompt_template | llm | parser

    response = chain.invoke(
        {
            "job_description": jd_txt,
        }
    )

    save_questions(response, candidate_id, jd_id, bu_id)
    print("Answer:\n", response)
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


def get_interview_questions_sytem_propmt_msg():
    """Instruct the system to follow this"""
    return """
    You are an AI assistant specialized in generating interview questions
    based on job description. Your goal is to provide a comprehensive and
    accurate set of questions that can be used to assess the suitability of a
    candidate for a particular job role. From the JD, just use the 'Skills'
    section to generate interview questions. DO NOT USE ANY OTHER SECTIONS

    Following are TODOs:
    * The questions should be of MCQs only
    * Each MCQ should contain just 4 options only
    * The candidate is having the time frame of just 30 minutes only. 
    * You provide the correct answer to the question also with the Option.
    * The questions complexity should be based on years of experinece needed
    * If needed experience is 0 ~ 1 year, the complexity should be low and should contain 28 questions.
    * If needed experience is 1 ~ 3 years, the complexity should be medium and should contain 25 questions.
    * If needed experience is 3 ~ 5 years, the complexity should be high and should contain 22 questions.
    * If needed experience is 5 ~ 8 years, the complexity should be more high and should contain 20 questions.
    * If needed experience is 8 ~ 11 years, the complexity should be tough and should contain 18 questions.
    * If needed experience is more than 11 years, the complexity should be critical and should contain 17 questions.
    * DO NOT PROVIDE the reason of why the answer is correct

    Provide the response in JSON format with the following fields
    * job_title
    * time_limit - This must be string which should contain minutes
    * instructions
    * questions_set - This should be list of questions. Please refer below how question format should be

    Each question in questions_set should be in JSON format with the following fields
    * question
    * options - This should be in the list format
    * correct_answer - This should contain just correct answer option

    """


def get_interview_questions_user_propmt_msg():
    """User prompt"""
    return """
            Please generate interview questions for a job description of {job_description}:
           """


def save_questions(response, candidate_id, jd_id, bu_id):
    """Save Questions"""
    correct_answer_list = "#END#".join(
        [
            f"{idx}:{question.correct_answer},"
            for idx, question in enumerate(response.questions_set)
        ]
    )
    save_question_answers_to_db(candidate_id, jd_id, bu_id, correct_answer_list)
