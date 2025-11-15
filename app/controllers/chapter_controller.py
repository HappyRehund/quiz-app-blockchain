from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.chapter_service import ChapterService
from app.controllers.auth_controller import get_current_user
from app.models.user import User


class ChapterController:
    @staticmethod
    async def get_course_chapters(
        course_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> dict:
        """Get all chapters for a course"""
        chapter_service = ChapterService(db)
        chapters = chapter_service.get_course_chapters(course_id, current_user.id)
        
        return {
            "success": True,
            "message": "Chapters retrieved successfully",
            "data": chapters
        }
    
    @staticmethod
    async def get_chapter_detail(
        chapter_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> dict:
        """Get chapter detail with content and quiz"""
        chapter_service = ChapterService(db)
        chapter = chapter_service.get_chapter_detail(chapter_id, current_user.id)
        
        return {
            "success": True,
            "message": "Chapter detail retrieved",
            "data": chapter
        }