from sqlalchemy.orm import Session
from app.repositories.certificate_repository import CertificateRepository
from app.repositories.progress_repository import ProgressRepository
from app.repositories.user_repository import UserRepository
from app.repositories.course_repository import CourseRepository
from app.services.blockchain_service import blockchain_service
from app.helpers.blockchain_helper import generate_certificate_id, generate_certificate_text, hash_certificate
from app.helpers.transaction_helper import transactional, read_only
from app.models.certificate import Certificate
from fastapi import HTTPException, status
from typing import List, Dict
from datetime import datetime


class CertificateService:
    def __init__(self, db: Session):
        self.db = db  # Simpan db session untuk transaction management
        self.cert_repo = CertificateRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.user_repo = UserRepository(db)
        self.course_repo = CourseRepository(db)
    
    @transactional
    def claim_certificate(self, user_id: int, course_id: int) -> Dict:
        """
        Claim certificate for completing course.
        """
        # Check if course exists
        course = self.course_repo.get_course_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Check user progress
        progress = self.progress_repo.get_progress(user_id, course_id)
        if not progress or progress.chapters_completed < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You must complete at least 2 chapters to claim certificate"
            )
        
        # Check if certificate already exists
        existing = self.cert_repo.check_existing_certificate(user_id, course_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Certificate already claimed for this course"
            )
        
        # Get user info
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Generate certificate data
        now = datetime.utcnow()
        cert_id = generate_certificate_id(user_id, course_id, now)
        cert_text = generate_certificate_text(
            cert_id=cert_id,
            user_id=user.id,
            username=user.username,
            email=user.email,
            created_at=now,
            chapters_completed=progress.chapters_completed
        )
        cert_hash = hash_certificate(cert_text)
        
        # Store on blockchain (jika gagal, exception akan di-raise dan DB rollback)
        blockchain_result = blockchain_service.store_certificate(cert_id, cert_hash)
        
        # Save to database (jika gagal, rollback)
        certificate = self.cert_repo.create_certificate(
            certificate_id=cert_id,
            user_id=user_id,
            course_id=course_id,
            chapters_completed=progress.chapters_completed,
            certificate_hash=cert_hash,
            tx_hash=blockchain_result["tx_hash"],
            block_number=blockchain_result["block_number"]
        )
        
        return {
            "id": certificate.id,
            "certificate_id": certificate.certificate_id,
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "course_id": course.id,
            "course_title": course.title,
            "chapters_completed": certificate.chapters_completed,
            "certificate_hash": certificate.certificate_hash,
            "tx_hash": certificate.tx_hash,
            "block_number": certificate.block_number,
            "created_at": certificate.created_at
        }
    
    @read_only
    def get_user_certificates(self, user_id: int) -> List[Dict]:
        """
        Get all certificates for a user.
        """
        certificates = self.cert_repo.get_user_certificates(user_id)
        result = []
        
        for cert in certificates:
            user = self.user_repo.get_user_by_id(cert.user_id)  # type: ignore
            course = self.course_repo.get_course_by_id(cert.course_id)  # type: ignore
            
            if not user or not course:
                continue
            
            result.append({
                "id": cert.id,
                "certificate_id": cert.certificate_id,
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "course_id": course.id,
                "course_title": course.title,
                "chapters_completed": cert.chapters_completed,
                "certificate_hash": cert.certificate_hash,
                "tx_hash": cert.tx_hash,
                "block_number": cert.block_number,
                "created_at": cert.created_at
            })
        
        return result
    
    @read_only
    def verify_certificate(self, certificate_id: str) -> Dict:
        """
        Verify certificate authenticity.
        """
        certificate = self.cert_repo.get_certificate_by_id(certificate_id)
        
        if not certificate:
            return {
                "is_valid": False,
                "certificate": None,
                "blockchain_timestamp": None,
                "message": "Certificate not found in database"
            }
        
        # Verify on blockchain
        blockchain_result = blockchain_service.verify_certificate(
            certificate_id, 
            certificate.certificate_hash
        )
        
        if not blockchain_result["is_valid"]:
            return {
                "is_valid": False,
                "certificate": None,
                "blockchain_timestamp": None,
                "message": "Certificate hash does not match blockchain record"
            }
        
        # Get full certificate data
        user = self.user_repo.get_user_by_id(certificate.user_id)  # type: ignore
        course = self.course_repo.get_course_by_id(certificate.course_id)  # type: ignore
        
        if not user or not course:
            return {
                "is_valid": False,
                "certificate": None,
                "blockchain_timestamp": None,
                "message": "Certificate data incomplete"
            }
        
        return {
            "is_valid": True,
            "certificate": {
                "id": certificate.id,
                "certificate_id": certificate.certificate_id,
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "course_id": course.id,
                "course_title": course.title,
                "chapters_completed": certificate.chapters_completed,
                "certificate_hash": certificate.certificate_hash,
                "tx_hash": certificate.tx_hash,
                "block_number": certificate.block_number,
                "created_at": certificate.created_at
            },
            "blockchain_timestamp": blockchain_result["timestamp"],
            "message": "Certificate is valid and verified on blockchain"
        }