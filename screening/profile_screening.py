"""Screening the profiles"""

import pathlib
import os

import docx
import pypdf as pdf
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from db.connect import get_jd_from_db
from file_utils import get_file_content, save_file_content
from llms.groq_gemma_llm import load_llm

TEMP_DIR = "temp"


class CandidateResult(BaseModel):
    """Candidate Result Model"""

    email: str
    name: str
    score: int
    details: list[str]


def profile_screen_results(jd_id, bu_id, resumes):
    """Do the screeing"""

    llm = load_llm()
    parser = JsonOutputParser()

    db_result = get_jd_from_db(jd_id, bu_id)
    file_name = db_result.get("title")
    file_content = db_result.get("doc")

    jd_txt = save_db_files_temporarily_and_get_delete(file_name, file_content)

    candidate_results = []
    for file in resumes:
        resume_txt = save_uploaded_files_temporarily_and_get_delete(file)

        prompt_template = ChatPromptTemplate(
            [
                (
                    "user",
                    get_profile_screen_propmt_msg(),
                ),
            ]
        )

        chain = prompt_template | llm | parser

        response = chain.invoke({"jd": jd_txt, "resume": resume_txt})
        candidate_results.append(
            CandidateResult(
                email=response.get("Candidate Email"),
                name=response.get("Candidate Name"),
                score=response.get("Score"),
                details=get_markdown_description(response.get("Description")),
            )
        )

    return sorted(candidate_results, key=lambda candidate: candidate.score)


def get_profile_screen_propmt_msg():
    """Getting screen profile prompt"""
    return """
            You are a skilled and very experienced software developer.
            You have a deep understanding of all technologies and programming languages.
            Your task is to evaluate the resume based on the given job description.
            As many will prepare resume based on the given job description and share it,
            you should strongly analyse the resume and provide the score of the provided resume.
            As we will filter the resume which are not mathing as per your analysis,
            think in all perspectives to calculate the score of the provided resume.

            Provide the response in the JSON format with the following fields
            * Candidate Name
            * Candidate Email
            * Score
            * Description - Providing the reason for the score. Please provide as List

            Following are the data you have been provided of resume and JD
            * Resume: {resume}
            * JD: {jd}
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


def save_db_files_temporarily_and_get_delete(file_name, file_content):
    """Storing temporarily uploaded files and retrieve text"""
    file_path = "".join([TEMP_DIR, "/", file_name])

    save_file_content(file_path=file_path, file_data=file_content)
    txt = get_file_content(file_path)
    os.remove(file_path)
    return txt


def get_doc_from_db(jd_id, bu_id):
    """Storing temporarily uploaded files and retrieve text"""
    file_path = "".join([TEMP_DIR, "/", uploaded_profile.filename])

    save_file_content(file_path=file_path, file_data=uploaded_profile.file.read())
    return get_file_content(file_path)


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
