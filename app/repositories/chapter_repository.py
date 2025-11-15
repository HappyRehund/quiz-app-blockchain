from sqlalchemy.orm import Session
from app.models.chapter import Chapter
from typing import List, Optional


class ChapterRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_chapter(
        self, 
        course_id: int, 
        chapter_number: int,
        title: str, 
        content: str,
        quiz_question: str,
        quiz_options: str,
        quiz_correct_answer: int
    ) -> Chapter:
        """Create a new chapter"""
        chapter = Chapter(
            course_id=course_id,
            chapter_number=chapter_number,
            title=title,
            content=content,
            quiz_question=quiz_question,
            quiz_options=quiz_options,
            quiz_correct_answer=quiz_correct_answer
        )
        self.db.add(chapter)
        self.db.flush()
        self.db.refresh(chapter)
        return chapter
    
    def get_chapters_by_course(self, course_id: int) -> List[Chapter]:
        """Get all chapters for a course"""
        return self.db.query(Chapter)\
            .filter(Chapter.course_id == course_id)\
            .order_by(Chapter.chapter_number)\
            .all()
    
    def get_chapter_by_id(self, chapter_id: int) -> Optional[Chapter]:
        """Get chapter by ID"""
        return self.db.query(Chapter).filter(Chapter.id == chapter_id).first()
    
    def count_chapters_by_course(self, course_id: int) -> int:
        """Count total chapters in a course"""
        return self.db.query(Chapter).filter(Chapter.course_id == course_id).count()