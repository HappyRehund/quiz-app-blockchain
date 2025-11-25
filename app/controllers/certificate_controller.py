from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.certificate_service import CertificateService
from app.services.blockchain_service import blockchain_service
from app.schemas.certificate_schema import CertificateCreate, CertificateVerify
from app.controllers.auth_controller import get_current_user
from app.models.user import User


class CertificateController:
    @staticmethod
    async def claim_certificate(
        cert_data: CertificateCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> dict:
        """Claim certificate for completing course"""
        cert_service = CertificateService(db)
        certificate = cert_service.claim_certificate(
            user_id=current_user.id,
            course_id=cert_data.course_id
        )
        
        return {
            "success": True,
            "message": "Certificate claimed and stored on blockchain",
            "data": certificate
        }
    
    @staticmethod
    async def get_my_certificates(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> dict:
        """Get all certificates for current user"""
        cert_service = CertificateService(db)
        certificates = cert_service.get_user_certificates(current_user.id)
        
        return {
            "success": True,
            "message": "Certificates retrieved successfully",
            "data": certificates
        }
    
    @staticmethod
    async def verify_certificate(
        verify_data: CertificateVerify,
        db: Session = Depends(get_db)
    ) -> dict:
        """Verify certificate authenticity (public endpoint)"""
        cert_service = CertificateService(db)
        result = cert_service.verify_certificate(verify_data.certificate_id)
        
        return {
            "success": result["is_valid"],
            "message": result["message"],
            "data": {
                "is_valid": result["is_valid"],
                "certificate": result["certificate"],
                "blockchain_timestamp": result["blockchain_timestamp"]
            }
        }
    
    @staticmethod
    async def debug_certificate(
        cert_id: str,
        db: Session = Depends(get_db)
    ) -> dict:
        cert_service = CertificateService(db)
        certificate = cert_service.cert_repo.get_certificate_by_id(cert_id)
        blockchain_hash = blockchain_service.get_certificate_hash(cert_id)
        
        return {
            "db_hash": certificate.certificate_hash if certificate else None,
            "blockchain_hash": blockchain_hash,
            "match": certificate.certificate_hash == blockchain_hash if certificate else False
        }