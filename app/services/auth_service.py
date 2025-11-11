from sqlalchemy.orm import Session
from app.helpers.password_helper import hash_password, verify_password
from app.helpers.jwt_helper import create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from fastapi import HTTPException, status
from typing import Tuple

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
    
    def register_user(self, username: str, email: str, password: str) -> User:
        """Register a new user"""
        
        # cek email
        if self.user_repo.get_user_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # cek username
        if self.user_repo.get_user_by_username(username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # hash password dan buat user
        hashed_password = hash_password(password)
        created_user = self.user_repo.create_user(username, email, hashed_password)
        
        return created_user
    
    def login_user(self, email: str, password: str) -> Tuple[str, User]:
        """Login user dan mendapatkan token jwt"""
        
        existing_user = self.user_repo.get_user_by_email(email)
        
        if not existing_user or not verify_password(password, str(existing_user.password_hash)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # buat token jwt
        access_token = create_access_token(
            data={
                "sub": str(existing_user.id),
                "email": existing_user.email
            }
        )
        
        return access_token, existing_user
    
    def get_current_user(self, user_id: int) -> User:
        """Get current authenticated user"""
        existing_user = self.user_repo.get_user_by_id(user_id)
        
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return existing_user