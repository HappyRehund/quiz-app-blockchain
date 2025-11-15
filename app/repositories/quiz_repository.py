from sqlalchemy.orm import Session
from app.models.quiz_answer import QuizAnswer
from typing import Optional, List


class QuizRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_or_update_answer(
        self, 
        user_id: int, 
        chapter_id: int, 
        answer_index: int,
        is_correct: bool
    ) -> QuizAnswer:
        """Create or update quiz answer"""
        answer = self.db.query(QuizAnswer)\
            .filter(QuizAnswer.user_id == user_id, QuizAnswer.chapter_id == chapter_id)\
            .first()
        
        if answer:
            answer.answer_index = answer_index
            answer.is_correct = is_correct
        else:
            answer = QuizAnswer(
                user_id=user_id,
                chapter_id=chapter_id,
                answer_index=answer_index,
                is_correct=is_correct
            )
            self.db.add(answer)
        
        self.db.flush()
        self.db.refresh(answer)
        return answer
    
    def get_user_answer(self, user_id: int, chapter_id: int) -> Optional[QuizAnswer]:
        """Get user's answer for a chapter"""
        return self.db.query(QuizAnswer)\
            .filter(QuizAnswer.user_id == user_id, QuizAnswer.chapter_id == chapter_id)\
            .first()
    
    def get_correct_answers_by_course(self, user_id: int, course_id: int) -> List[QuizAnswer]:
        """Get all correct answers for a course"""
        from app.models.chapter import Chapter
        return self.db.query(QuizAnswer)\
            .join(Chapter, QuizAnswer.chapter_id == Chapter.id)\
            .filter(
                QuizAnswer.user_id == user_id,
                Chapter.course_id == course_id,
                QuizAnswer.is_correct == True
            ).all()