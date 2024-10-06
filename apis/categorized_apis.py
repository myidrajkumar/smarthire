"""APIs which are used across but could not be categorized"""

import secrets
from fastapi import APIRouter

from db.connect import get_business_units, get_jds_for_bu_db, save_candidate_credentials
from utils.email_utils import send_exam_email

router = APIRouter()


@router.get("/businessunits")
async def get_businessunits():
    """Retrieving business units"""

    results = get_business_units()
    return {"message": "Success", "data": results}


@router.get("/businessunits/{bu_id}/jds")
async def get_jds_for_bu(bu_id):
    """Getting JD titles for a specific BU"""

    results = get_jds_for_bu_db(bu_id)
    return {"message": "Success", "data": results}


@router.post("/generatecredentials/{candidateid}")
async def generate_credentials(candidateid: int):
    """Generating Credentials"""
    username = f"user_{secrets.token_hex(4)}"
    password = secrets.token_hex(8)
    save_candidate_credentials(candidateid, username, password)
    send_exam_email("myidrajkumar@gmail.com", "test", username, password)
    return {"username": username, "password": password}
