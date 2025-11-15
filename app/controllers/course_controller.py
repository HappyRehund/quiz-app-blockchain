from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.course_service import CourseService
from app.controllers.auth_controller import get_current_user
from app.models.user import User


class CourseController:
    @staticmethod
    async def get_all_courses(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> dict:
        """Get all available courses"""
        course_service = CourseService(db)
        courses = course_service.get_all_courses(current_user.id)
        
        return {
            "success": True,
            "message": "Courses retrieved successfully",
            "data": courses
        }
    
    @staticmethod
    async def get_course_detail(
        course_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> dict:
        """Get course detail"""
        course_service = CourseService(db)
        course = course_service.get_course_detail(course_id, current_user.id)
        
        return {
            "success": True,
            "message": "Course detail retrieved",
            "data": course
        }