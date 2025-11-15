from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CertificateCreate(BaseModel):
    course_id: int


class CertificateResponse(BaseModel):
    id: int
    certificate_id: str
    user_id: int
    username: str
    email: str
    course_id: int
    course_title: str
    chapters_completed: int
    certificate_hash: str
    tx_hash: Optional[str]
    block_number: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class CertificateVerify(BaseModel):
    certificate_id: str


class CertificateVerifyResponse(BaseModel):
    is_valid: bool
    certificate: Optional[CertificateResponse]
    blockchain_timestamp: Optional[int]
    message: str