from sqlalchemy.orm import Session
from app.models.certificate import Certificate
from typing import Optional, List


class CertificateRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_certificate(
        self,
        certificate_id: str,
        user_id: int,
        course_id: int,
        chapters_completed: int,
        certificate_hash: str,
        tx_hash: Optional[str] = None,
        block_number: Optional[int] = None
    ) -> Certificate:
        """Create a new certificate"""
        certificate = Certificate(
            certificate_id=certificate_id,
            user_id=user_id,
            course_id=course_id,
            chapters_completed=chapters_completed,
            certificate_hash=certificate_hash,
            tx_hash=tx_hash,
            block_number=block_number
        )
        self.db.add(certificate)
        self.db.commit()
        self.db.refresh(certificate)
        return certificate
    
    def get_certificate_by_id(self, certificate_id: str) -> Optional[Certificate]:
        """Get certificate by certificate_id"""
        return self.db.query(Certificate)\
            .filter(Certificate.certificate_id == certificate_id)\
            .first()
    
    def get_user_certificates(self, user_id: int) -> List[Certificate]:
        """Get all certificates for a user"""
        return self.db.query(Certificate)\
            .filter(Certificate.user_id == user_id)\
            .order_by(Certificate.created_at.desc())\
            .all()
    
    def check_existing_certificate(self, user_id: int, course_id: int) -> Optional[Certificate]:
        """Check if user already has certificate for course"""
        return self.db.query(Certificate)\
            .filter(Certificate.user_id == user_id, Certificate.course_id == course_id)\
            .first()