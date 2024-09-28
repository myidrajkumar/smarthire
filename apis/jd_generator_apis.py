"""JD Generator APIs"""

import os
from typing import Optional

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel

from db.connect import get_business_units, save_doc_db
from utils.file_utils import get_file_content_binary
from jd_handling.jd_generator import get_jd_from_model_json
from jd_handling.jd_persister import save_jd_and_retrieve

router = APIRouter()


class JobDescriptionRequest(BaseModel):
    """Request Parameters"""

    bu_id: Optional[int] = None
    job_title: str
    experience: str
    skills: str


@router.post("/generatejd")
async def generate_jd(request: JobDescriptionRequest):
    """Generating PDF Response"""
    llm_response = get_jd_from_model_json(
        request.job_title, request.skills, request.experience
    )
    print("LLM Response", llm_response)
    file_path = save_jd_and_retrieve(llm_response, bu_id=request.bu_id)
    print("Job Description generated successfully!!!")
    return {"message": "Success", "file_name": file_path}


@router.get("/download")
async def download_jd(
    f_name: str,
    f_type: str,
    bu_id: Optional[int] = None,
):
    """Serving PDF Response"""
    # background_tasks.add_task(delete_file, f"docs/{f_name}")

    bu_name = get_business_units(bu_id)[0].get("name")
    folder_path = "".join(["docs", "/", bu_name])

    file_response = None
    if f_type.endswith("txt"):
        f_name += ".txt"
        file_response = FileResponse(f"{folder_path}/{f_name}", filename=f_name)
    elif f_type.endswith("pdf"):
        f_name += ".pdf"
        file_response = FileResponse(f"{folder_path}/{f_name}", filename=f_name)
    else:
        f_name += ".docx"
        file_response = FileResponse(f"{folder_path}/{f_name}", filename=f_name)

    file_response.headers["Content-Disposition"] = "inline"
    file_response.headers["filename"] = f_name
    return file_response


@router.get("/savejd")
async def savejd(
    background_tasks: BackgroundTasks,
    bu_id: int,
    jd_title: str,
    is_save: bool,
):
    """Saving the doc to DB"""

    if not is_save:
        return {"message": "Success"}

    # Get specific BU
    bu_details_list = get_business_units(bu_id)
    bu_name = bu_details_list[0].get("name")

    # Read the doc from BU folder
    file_path_to_be_read = "".join(["docs", "/", bu_name, "/", (f"{jd_title}")])
    doc_content = get_file_content_binary(file_path_to_be_read)
    if doc_content is None:
        return {"message": "Failure"}

    # Save the doc to DB
    save_doc_db(bu_id, jd_title, doc_content)
    background_tasks.add_task(delete_file, f"{file_path_to_be_read}")
    return {"message": "Success"}


def delete_file(file_path: str):
    """Deleting the generated files"""
    try:
        file_path = file_path[0 : file_path.rfind(".")]
        os.remove(f"{file_path}.pdf")
        os.remove(f"{file_path}.docx")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
