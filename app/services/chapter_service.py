from sqlalchemy.orm import Session
from app.repositories.chapter_repository import ChapterRepository
from app.repositories.quiz_repository import QuizRepository
from app.repositories.course_repository import CourseRepository
from app.models.chapter import Chapter
from fastapi import HTTPException, status
from typing import List, Dict
import json


class ChapterService:
    def __init__(self, db: Session):
        self.chapter_repo = ChapterRepository(db)
        self.quiz_repo = QuizRepository(db)
        self.course_repo = CourseRepository(db)
    
    def get_course_chapters(self, course_id: int, user_id: int) -> List[Dict]:
        """Get all chapters for a course with completion status"""
        course = self.course_repo.get_course_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        chapters = self.chapter_repo.get_chapters_by_course(course_id)
        result = []
        
        for chapter in chapters:
            answer = self.quiz_repo.get_user_answer(user_id, chapter.id)
            is_completed = answer.is_correct if answer else False
            
            result.append({
                "id": chapter.id,
                "chapter_number": chapter.chapter_number,
                "title": chapter.title,
                "is_completed": is_completed
            })
        
        return result
    
    def get_chapter_detail(self, chapter_id: int, user_id: int) -> Dict:
        """Get chapter detail with content and quiz"""
        chapter = self.chapter_repo.get_chapter_by_id(chapter_id)
        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )
        
        answer = self.quiz_repo.get_user_answer(user_id, chapter.id)
        is_completed = answer.is_correct if answer else False
        
        return {
            "id": chapter.id,
            "course_id": chapter.course_id,
            "chapter_number": chapter.chapter_number,
            "title": chapter.title,
            "content": chapter.content,
            "quiz_question": chapter.quiz_question,
            "quiz_options": json.loads(chapter.quiz_options),
            "is_completed": is_completed
        }