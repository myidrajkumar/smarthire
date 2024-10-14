"""Credentials API"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.connect import validate_user_credentials

router = APIRouter()


class CandidateUser(BaseModel):
    """Request Parameters"""

    username: str
    password: str


@router.post("/login")
async def candidate_login(request: CandidateUser):
    """Login the user"""

    candidate_details = validate_user_credentials(request.username, request.password)

    if not candidate_details:
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    if candidate_details.get("expired"):
        raise HTTPException(status_code=403, detail="You already attended the exam")

    return {"message": "Success", "data": candidate_details}
