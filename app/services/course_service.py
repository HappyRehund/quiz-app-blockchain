from sqlalchemy.orm import Session
from app.repositories.course_repository import CourseRepository
from app.repositories.chapter_repository import ChapterRepository
from app.repositories.progress_repository import ProgressRepository
from app.models.course import Course
from fastapi import HTTPException, status
from typing import List, Dict


class CourseService:
    def __init__(self, db: Session):
        self.course_repo = CourseRepository(db)
        self.chapter_repo = ChapterRepository(db)
        self.progress_repo = ProgressRepository(db)
    
    def get_all_courses(self, user_id: int) -> List[Dict]:
        """Get all courses with user progress"""
        courses = self.course_repo.get_all_courses()
        result = []
        
        for course in courses:
            total_chapters = self.chapter_repo.count_chapters_by_course(course.id)
            progress = self.progress_repo.get_progress(user_id, course.id)
            user_progress = progress.chapters_completed if progress else 0
            
            result.append({
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "total_chapters": total_chapters,
                "user_progress": user_progress
            })
        
        return result
    
    def get_course_detail(self, course_id: int, user_id: int) -> Dict:
        """Get course detail with user progress"""
        course = self.course_repo.get_course_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        total_chapters = self.chapter_repo.count_chapters_by_course(course.id)
        progress = self.progress_repo.get_progress(user_id, course.id)
        user_progress = progress.chapters_completed if progress else 0
        
        return {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "created_at": course.created_at,
            "total_chapters": total_chapters,
            "user_progress": user_progress
        }