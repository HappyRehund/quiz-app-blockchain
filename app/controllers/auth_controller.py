from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_schema import UserLogin, UserRegister, UserResponse, TokenResponse
from app.helpers.jwt_helper import decode_access_token
from app.models.user import User

security = HTTPBearer()

class AuthController:
    @staticmethod
    async def register(user_data: UserRegister, db: Session = Depends(get_db)) -> dict:
        """Register user baru"""
        
        return {
            "success": True,
            "message": "User registered successfully",
            "data": user_data
        }
    
    @staticmethod
    async def login(credentials: UserLogin, db: Session = Depends(get_db)) -> dict:
        """Login user"""
        
        return {
            "success": True,
            "message": "Login successful"
        }
    
    @staticmethod
    async def get_current_user_from_token(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ) -> str :
        
        return "Suksesin aja dulu"
    
    @staticmethod
    async def get_me(current_user: User = Depends(get_current_user_from_token)) -> dict:
        """Get current user profile"""
        return {
            "success": True,
            "message": "User profile retrieved"
        }

# Dependency for protected routes
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> str:
    return "pentil" 