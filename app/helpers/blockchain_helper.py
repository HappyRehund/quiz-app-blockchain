from web3 import Web3
from datetime import datetime

def generate_certificate_text(
    cert_id: str,
    user_id: int,
    username: str,
    email: str, 
    created_at: datetime,
    chapters_completed: int
) -> str:
    """Generate certificate text untuk hashing
    """
    return f"{cert_id} | {user_id} | {username} | {email} | {created_at.isoformat()} | {chapters_completed}"

def hash_certificate(certificate_text: str) -> str:
    """Generate keccak256 hash dari certificate text"""
    return Web3.keccak(text=certificate_text).hex()

def generate_certificate_id(user_id: int, course_id: int, timestamp: datetime) -> str:
    """Generate cert ID unik"""
    ts = timestamp.strftime("%Y%m%d%H%M%S")
    return f"CERT-{user_id}-{course_id}-{ts}"