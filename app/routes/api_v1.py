from fastapi import APIRouter, Depends
from app.controllers.auth_controller import AuthController, get_current_user
from app.controllers.course_controller import CourseController
from app.controllers.chapter_controller import ChapterController
from app.controllers.quiz_controller import QuizController
from app.controllers.certificate_controller import CertificateController
from app.schemas.user_schema import UserRegister, UserLogin
from app.schemas.quiz_schema import QuizSubmit
from app.schemas.certificate_schema import CertificateCreate, CertificateVerify
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1")

# Bagian AUTH
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register")
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    return await AuthController.register(user_data, db)

@auth_router.post("/login")
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    return await AuthController.login(credentials, db)

@auth_router.get("/me")
async def get_me(
    current_user = Depends(get_current_user)
):
    return await AuthController.get_me(current_user)

router.include_router(auth_router)

# Bagian COURSE
course_router = APIRouter(prefix="/courses", tags=["Courses"])

@course_router.get("")
async def get_all_courses(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await CourseController.get_all_courses(current_user, db)

@course_router.get("/{course_id}")
async def get_course_detail(
    course_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await CourseController.get_course_detail(course_id, current_user, db)

router.include_router(course_router)

# Bagian CHAPTER
chapter_router = APIRouter(prefix="/chapters", tags=["Chapters"])

@chapter_router.get("/course/{course_id}")
async def get_course_chapters(
    course_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ChapterController.get_course_chapters(course_id, current_user, db)

@chapter_router.get("/{chapter_id}")
async def get_chapter_detail(
    chapter_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ChapterController.get_chapter_detail(chapter_id, current_user, db)

router.include_router(chapter_router)

# Bagian QUIZ
quiz_router = APIRouter(prefix="/quiz", tags=["Quiz"])

@quiz_router.post("/submit")
async def submit_quiz(
    quiz_data: QuizSubmit,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await QuizController.submit_quiz(quiz_data, current_user, db)

router.include_router(quiz_router)

# Bagian CERTIFICATE
certificate_router = APIRouter(prefix="/certificates", tags=["Certificates"])

@certificate_router.post("/claim")
async def claim_certificate(
    cert_data: CertificateCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await CertificateController.claim_certificate(cert_data, current_user, db)

@certificate_router.get("/my-certificates")
async def get_my_certificates(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await CertificateController.get_my_certificates(current_user, db)

@certificate_router.post("/verify")
async def verify_certificate(
    verify_data: CertificateVerify,
    db: Session = Depends(get_db)
):
    return await CertificateController.verify_certificate(verify_data, db)

@certificate_router.get("/debug/{cert_id}")
async def debug_certificate(
    cert_id: str,
    db: Session = Depends(get_db)
):
    return await CertificateController.debug_certificate(cert_id, db)

router.include_router(certificate_router)