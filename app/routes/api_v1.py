from fastapi import APIRouter, Depends
from app.controllers.auth_controller import AuthController
from app.schemas.user_schema import UserRegister, UserLogin

router = APIRouter(prefix="/api/v1")

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register")
async def register(user_data: UserRegister, db=Depends()):
    return None;