"""Candidate Model"""

from typing import Optional
from pydantic import BaseModel


class Candidate(BaseModel):
    """Candidate Result Model"""

    id: Optional[int] = None
    email: str
    name: str
    phone: str
    resume: Optional[str] = None
