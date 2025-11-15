from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.quiz_service import QuizService
from app.schemas.quiz_schema import QuizSubmit
from app.controllers.auth_controller import get_current_user
from app.models.user import User


class QuizController:
    @staticmethod
    async def submit_quiz(
        quiz_data: QuizSubmit,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> dict:
        """Submit quiz answer"""
        quiz_service = QuizService(db)
        result = quiz_service.submit_quiz_answer(
            user_id=current_user.id,
            chapter_id=quiz_data.chapter_id,
            answer_index=quiz_data.answer_index
        )
        
        return {
            "success": True,
            "message": result["message"],
            "data": result
        }