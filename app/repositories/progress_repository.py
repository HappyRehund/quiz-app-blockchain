from sqlalchemy.orm import Session
from app.models.user_progress import UserProgress
from typing import Optional


class ProgressRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_progress(self, user_id: int, course_id: int) -> UserProgress:
        """Get or create user progress for a course"""
        progress = self.db.query(UserProgress)\
            .filter(UserProgress.user_id == user_id, UserProgress.course_id == course_id)\
            .first()
        
        if not progress:
            progress = UserProgress(
                user_id=user_id,
                course_id=course_id,
                chapters_completed=0
            )
            self.db.add(progress)
            self.db.commit()
            self.db.refresh(progress)
        
        return progress
    
    def update_progress(self, user_id: int, course_id: int, chapters_completed: int) -> UserProgress:
        """Update user progress"""
        progress = self.get_or_create_progress(user_id, course_id)
        progress.chapters_completed = chapters_completed
        self.db.commit()
        self.db.refresh(progress)
        return progress
    
    def get_progress(self, user_id: int, course_id: int) -> Optional[UserProgress]:
        """Get user progress for a course"""
        return self.db.query(UserProgress)\
            .filter(UserProgress.user_id == user_id, UserProgress.course_id == course_id)\
            .first()