"""Serive to handle preliminary"""

import os
from typing import List

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from db.connect import (
    get_answers_from_db,
    get_candidate_from_db,
    get_interview_questions_from_db,
    get_jd_from_db,
    remove_candidate_questions_from_db,
    save_candidate_credentials,
    save_question_answers_to_db,
    update_candidate_preliminary_interview_status_db,
)
from llms.groq_llama_llm import load_llm
from utils.credential_utils import generate_credentials
from utils.email_utils import send_exam_email
from utils.file_utils import save_files_temporarily_and_get_delete


class Question(BaseModel):
    """Questions"""

    question: str
    options: List[str]
    correct_answer: str


class Candidate(BaseModel):
    """Candidate"""

    questions_set: List[Question]


class QuestionsSet(BaseModel):
    """Questions Set"""

    job_title: str
    time_limit: str
    instructions: str
    candidates_set: list[Candidate]


def generate_interview_questions(jd_txt, candidate_count):
    """Get Interview Questions"""
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
            "candidate_count": candidate_count,
        }
    )

    return response


def get_interview_questions_sytem_propmt_msg():
    """Instruct the system to follow this"""
    # 28, 25, 22, 20, 18, 17
    return """
    You are an AI assistant specialized in generating interview questions
    based on job description. Your goal is to provide a comprehensive and
    accurate set of questions that can be used to assess the suitability of a
    candidates for a particular job role. From the JD, just use the 'Skills'
    section to generate interview questions. DO NOT USE ANY OTHER SECTIONS

    Following are TODOs:
    * The questions should be of MCQs only
    * Each MCQ should contain just 4 options only
    * The candidates are having the time frame of just 30 minutes only.
    * You provide the correct answer to the question also with the Option.
    * The questions complexity should be based on years of experinece needed
    * If needed experience is 0 ~ 1 year, the complexity should be low and should contain 28 questions.
    * If needed experience is 1 ~ 3 years, the complexity should be medium and should contain 25 questions.
    * If needed experience is 3 ~ 5 years, the complexity should be high and should contain 22 questions.
    * If needed experience is 5 ~ 8 years, the complexity should be more high and should contain 20 questions.
    * If needed experience is 8 ~ 11 years, the complexity should be tough and should contain 18 questions.
    * If needed experience is more than 11 years, the complexity should be critical and should contain 17 questions.
    * DO NOT PROVIDE the reason of why the answer is correct

    Each item in the list has to be in JSON format with the following fields
    * job_title
    * time_limit - This must be string which should contain minutes
    * instructions
    * candidates_set - This should be list of candidates. Please refer below how candidate format should be

    Each candidate should contain list of questions and SHOULD NOT CONTAIN any other fields.
    * questions_set - This should be list of questions. Please refer below how question format should be

    Each question in questions list should be in JSON format with the following fields
    * question
    * options - This should be in the list format
    * correct_answer - This should contain EXACT CORRECT ANSWER VALUE and it should not be option value

    """


def get_interview_questions_user_propmt_msg():
    """User prompt"""
    return """
            Please generate interview questions for a job description of {job_description}
            and generate the questions to the candidate count of {candidate_count}
           """


def save_questions(response, candidate_list, jd_id, bu_id):
    """Save Questions"""

    save_question_answers_to_db(candidate_list, jd_id, bu_id, response)


def get_jd_doc(jd_id, bu_id):
    """Get JD from DB"""
    db_result = get_jd_from_db(jd_id, bu_id)
    file_name = f'{db_result.get("title")}.docx'
    jd_txt = save_files_temporarily_and_get_delete(file_name, db_result.get("doc"))

    return jd_txt


def get_interview_questions(jd_id, bu_id, candidate_id):
    """Get Questions"""
    db_result = get_interview_questions_from_db(jd_id, bu_id, candidate_id)
    assigned_questions = [
        {
            "question": row["question"],
            "options": [row[f"option{i}"] for i in range(1, 5)],
        }
        for row in db_result
    ]
    return assigned_questions


class CandidateEmail(BaseModel):
    """Candidate Email"""

    name: str
    username: str
    password: str
    exam_link: str
    email: str


def generate_credentials_and_send_email(candidate_list, jd_id, bu_id):
    """Generate credentials and send email"""
    for candidate_id in candidate_list:
        username, password = generate_credentials()
        save_candidate_credentials(candidate_id, username, password)

        candidate_result = get_candidate_from_db(candidate_id)
        host_url = os.getenv("HOST_URL", "http://127.0.0.1:8000")

        candidate = CandidateEmail(
            name=candidate_result.get("name"),
            username=username,
            password=password,
            exam_link=f"{host_url}/triggerexam?jd_id={jd_id}&bu_id={bu_id}&candidate_id={candidate_id}",
            email=candidate_result.get("email"),
        )
        try:
            send_exam_email(candidate)
        except Exception as error:
            print(f"ERROR: Email could not be sent: {error}")


def get_answers(candidate_id, jd_id, bu_id):
    """Getting answers"""
    db_results = get_answers_from_db(candidate_id, jd_id, bu_id)
    return [row.get("answer") for row in db_results]


def update_candidate_preliminart_interview_status(jd_id, bu_id, candidate_list):
    """Update the status of the candidates"""
    status = "Preliminary: Invite Sent"
    update_candidate_preliminary_interview_status_db(
        jd_id, bu_id, candidate_list, status
    )


def remove_candidate_questions(candidate_id: int, jd_id: int, bu_id: int):
    """Removing Candidate Questions"""
    remove_candidate_questions_from_db(candidate_id, jd_id, bu_id)
