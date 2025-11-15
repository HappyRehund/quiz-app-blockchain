from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_schema import UserLogin, UserRegister, UserResponse, TokenResponse
from app.helpers.jwt_helper import decode_access_token
from app.models.user import User
from app.services.auth_service import AuthService

security = HTTPBearer()

class AuthController:
    @staticmethod
    async def register(
        user_data: UserRegister, 
        db: Session = Depends(get_db)
    ) -> dict:
        """Register user baru"""
        auth_service = AuthService(db)
        
        user = auth_service.register_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )


        return {
            "success": True,
            "message": "User registered successfully",
            "data": UserResponse.model_validate(user)
        }
    
    @staticmethod
    async def login(
        credentials: UserLogin,
        db: Session = Depends(get_db)
    ) -> dict:
        """Login user"""
        
        auth_service = AuthService(db)
        access_token, user = auth_service.login_user(
            email=credentials.email,
            password=credentials.password
        )

        return {
            "success": True,
            "message": "Login successful",
            "data": TokenResponse(
                access_token=access_token,
                user=UserResponse.model_validate(user)
            )
        }
    
    @staticmethod
    async def get_current_user_from_token(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ) -> User :
        """Get current user dari JWT token"""
        token = credentials.credentials
        payload = decode_access_token(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        user_id: int = int(user_id_str)
        auth_service = AuthService(db)

        return auth_service.get_current_user(user_id)

    @staticmethod
    async def get_me(
        current_user: User = Depends(get_current_user_from_token)
    ) -> dict:
        """Get current user profile"""
        return {
            "success": True,
            "message": "User profile retrieved",
            "data": UserResponse.model_validate(current_user)
        }

# Dependency for protected routes
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    
    return await AuthController.get_current_user_from_token(credentials, db)