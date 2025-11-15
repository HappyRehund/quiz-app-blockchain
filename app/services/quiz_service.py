from sqlalchemy.orm import Session
from app.repositories.chapter_repository import ChapterRepository
from app.repositories.quiz_repository import QuizRepository
from app.repositories.progress_repository import ProgressRepository
from fastapi import HTTPException, status
from typing import Dict


class QuizService:
    def __init__(self, db: Session):
        self.chapter_repo = ChapterRepository(db)
        self.quiz_repo = QuizRepository(db)
        self.progress_repo = ProgressRepository(db)
    
    def submit_quiz_answer(self, user_id: int, chapter_id: int, answer_index: int) -> Dict:
        """Submit quiz answer and update progress"""
        chapter = self.chapter_repo.get_chapter_by_id(chapter_id)
        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )
        
        # Check if answer is correct
        is_correct = (answer_index == chapter.quiz_correct_answer)
        
        # Save answer
        self.quiz_repo.create_or_update_answer(
            user_id=user_id,
            chapter_id=chapter_id,
            answer_index=answer_index,
            is_correct=is_correct
        )
        
        # Update progress if answer is correct
        if is_correct:
            correct_answers = self.quiz_repo.get_correct_answers_by_course(
                user_id, 
                chapter.course_id
            )
            chapters_completed = len(correct_answers)
            
            self.progress_repo.update_progress(
                user_id=user_id,
                course_id=chapter.course_id,
                chapters_completed=chapters_completed
            )
        
        message = "Correct answer!" if is_correct else "Wrong answer. Please try again."
        
        return {
            "is_correct": is_correct,
            "correct_answer_index": chapter.quiz_correct_answer,
            "message": message
        }