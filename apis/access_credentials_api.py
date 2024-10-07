"""Credentials API"""

import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from db.connect import validate_user_credentials

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY", "DummySecretKey")
router = APIRouter()


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login the user"""

    is_valid_user = validate_user_credentials(form_data.username, form_data.password)

    if not is_valid_user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    token = jwt.encode({"sub": form_data.username}, SECRET_KEY)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/secureexam/")
async def secure_exam(token: str = Depends(oauth2_scheme)):
    """Inititate the exam"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        # Verify the token and grant access
        return {"message": f"Welcome {username}, to your exam!"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
