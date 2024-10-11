"""Screening the profiles"""

import os
import pathlib
from typing import List, Optional

import docx
import pypdf as pdf
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, RootModel

from db.connect import (
    get_jd_from_db,
    get_screened_candidates,
    save_candidate_details,
    save_all_candidates_scores_with_status,
    update_candidate_interview_status,
)
from llms.groq_gemma_llm import load_llm
from models.candidate import Candidate
from utils.file_utils import (
    get_file_content,
    save_file_content,
    save_files_temporarily_and_get_delete,
)

TEMP_DIR = "temp"


class CandidateResult(BaseModel):
    """Candidate Result Model"""

    id: Optional[int] = None
    email: str
    name: str
    phone: str
    score: int
    details: list[str]


class CandidatesList(RootModel):
    """Candidates List"""

    root: List[CandidateResult]


def profile_screen_results(jd_id, bu_id, resumes):
    """Do the screeing"""

    llm = load_llm()
    parser = PydanticOutputParser(pydantic_object=CandidatesList)

    db_result = get_jd_from_db(jd_id, bu_id)
    file_name = f"{db_result.get('title')}.docx"
    jd_txt = save_files_temporarily_and_get_delete(file_name, db_result.get("doc"))

    candidate_details = get_candidate_details(resumes)
    candidate_details = save_candidate_details(
        jd_id=jd_id, bu_id=bu_id, candidate_details_list=candidate_details
    )
    resumes_list = [candidate.resume for candidate in candidate_details]

    prompt_template = ChatPromptTemplate(
        [
            (
                "system",
                get_profile_screen_system_prompt_msg(),
            ),
            (
                "system",
                "Include only candidates result as list. Please DO NOT provide any other information",
            ),
            (
                "user",
                get_profile_screen_user_propmt_msg(),
            ),
        ]
    )

    chain = prompt_template | llm | parser

    response = chain.invoke({"jd": jd_txt, "resume_list": resumes_list})
    candidate_results = response.root

    for candidate in candidate_results:
        candidate.id = [
            saved_candidate.id
            for saved_candidate in candidate_details
            if saved_candidate.email == candidate.email
        ][0]
    save_all_candidates_scores_with_status(candidate_results, "Screened")
    return sorted(
        candidate_results, key=lambda candidate: candidate.score, reverse=True
    )


def get_profile_screen_user_propmt_msg():
    """Getting screen profile prompt"""
    return """
            Following are the data you have been provided of resumes and JD
            * ResumeList: {resume_list}
            * JD: {jd}
           """


def get_candidate_details_user_propmt_msg():
    """Getting candidate details prompt"""
    return """
            Resume: {resume}
           """


def get_profile_screen_system_prompt_msg():
    """Getting screen profile prompt"""
    return """
            You are a skilled and very experienced software developer.
            You have a deep understanding of all technologies and programming languages.
            Your task is to evaluate the resumes based on the given job description.
            As many will prepare resume based on the given job description and share it,
            you should strongly analyse the resume and provide the score of the provided resume.
            As we will filter the resume which are not matching as per your analysis,
            think in all perspectives to calculate the score of the provided resume.

            Provide the response in the List of JSON format.
            The each item in the list should contain only the following fields
            * name
            * email - Please keep blank if not available
            * phone - Please keep blank if not available
            * score - Provide the score out of 100
            * details - Providing the reason for the score. This has to be crisp and attractive. Please provide as List
           """


def get_candidate_details_system_prompt_msg():
    """Getting candidate details prompt"""
    return """
            You need to analyse the resume and get the candidate details.

            Provide the response in the JSON format only and should contain only the following fields.
            * name
            * email - Please keep blank if not available
            * phone - Please keep blank if not available
           """


def get_profile_info_pdf(uploaded_profile):
    """Get content from PDF file"""

    file_path = save_uploaded_files_temporarily(uploaded_profile)

    reader = pdf.PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += str(page.extract_text())
    return text


def save_uploaded_files_temporarily(uploaded_profile):
    """Storing temporarily uploaded files"""
    file_path = "".join([TEMP_DIR, "/", uploaded_profile.filename])
    pathlib.Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "wb") as file:
        file.write(uploaded_profile.file.read())
        print(f"File '{file_path}' saved.")
    return file_path


def save_uploaded_files_temporarily_and_get_delete(uploaded_profile):
    """Storing temporarily uploaded files and retrieve text"""
    file_path = "".join([TEMP_DIR, "/", uploaded_profile.filename])

    save_file_content(file_path=file_path, file_data=uploaded_profile.file.read())
    txt = get_file_content(file_path)
    os.remove(file_path)
    return txt


def get_jd_info_docx(uploaded_jd):
    """Get content from docx file"""
    file_path = save_uploaded_files_temporarily(uploaded_jd)

    doc = docx.Document(file_path)
    text = ""

    for para in doc.paragraphs:
        text += para.text
    return text


def get_markdown_description(description):
    """Convert to markdown"""
    return [each_desc for each_desc in description]


def get_candidate_details(resumes):
    """Get candidate details"""

    llm = load_llm()
    parser = PydanticOutputParser(pydantic_object=Candidate)

    prompt_template = ChatPromptTemplate(
        [
            (
                "system",
                get_candidate_details_system_prompt_msg(),
            ),
            (
                "system",
                "Include only candidates details. Please DO NOT provide any other information",
            ),
            (
                "user",
                get_candidate_details_user_propmt_msg(),
            ),
        ]
    )

    chain = prompt_template | llm | parser

    candidate_details_list = []
    for each_resume in resumes:
        resume_text = save_uploaded_files_temporarily_and_get_delete(each_resume)
        response = chain.invoke({"resume": resume_text})
        candidate_details = response
        candidate_details.resume = resume_text
        candidate_details_list.append(candidate_details)

    return candidate_details_list


def save_selected_candidates(jd_id, bu_id, candidate_status):
    """Selecting first round candidates"""

    for candidate in candidate_status:
        candidate.interview_status = (
            f"Screening: {'Selected' if candidate.status else 'Rejected'}"
        )

    update_candidate_interview_status(jd_id, bu_id, candidate_status)


def get_selected_candidates(jd_id, bu_id, status=None):
    """Selecting first round candidates"""
    return get_screened_candidates(jd_id, bu_id, status)
