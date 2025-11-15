from fastapi import APIRouter, Depends
from app.controllers.auth_controller import AuthController
from app.controllers.course_controller import CourseController
from app.controllers.chapter_controller import ChapterController
from app.schemas.user_schema import UserRegister, UserLogin

router = APIRouter(prefix="/api/v1")

# Bagian AUTH
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register")
async def register(
    user_data: UserRegister,
    db=Depends()
):
    return await AuthController.register(user_data, db);

@auth_router.post("/login")
async def login(
    credentials: UserLogin,
    db=Depends()
):
    return await AuthController.login(credentials, db);

@auth_router.get("/me")
async def get_me(
    current_user=Depends(AuthController.get_current_user_from_token)
):
    return await AuthController.get_me(current_user);

router.include_router(auth_router)

# Bagian COURSE
course_router = APIRouter(prefix="/courses", tags=["Courses"])

@course_router.get("")
async def get_all_courses(
    current_user=Depends(),
    db=Depends()
):
    return await CourseController.get_all_courses(current_user, db)

@course_router.get("/{course_id}")
async def get_course_detail(
    course_id: int,
    current_user=Depends(),
    db=Depends()
):
    return await CourseController.get_course_detail(course_id, current_user, db)

router.include_router(course_router)

# Bagian CHAPTER
chapter_router = APIRouter(prefix="/chapters", tags=["Chapters"])

@chapter_router.get("/course/{course_id}")
async def get_course_chapters(
    course_id: int,
    current_user=Depends(),
    db=Depends()
):
    return await ChapterController.get_course_chapters(course_id, current_user, db)

@chapter_router.get("/{chapter_id}")
async def get_chapter_detail(
    chapter_id: int,
    current_user=Depends(),
    db=Depends()
):
    return await ChapterController.get_chapter_detail(chapter_id, current_user, db)

router.include_router(chapter_router)