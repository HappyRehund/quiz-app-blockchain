# Import all models here to ensure they're registered with SQLAlchemy
from app.models.user import User
from app.models.course import Course
from app.models.chapter import Chapter
from app.models.user_progress import UserProgress
from app.models.quiz_answer import QuizAnswer
from app.models.certificate import Certificate

# Export all models
__all__ = [
    "User",
    "Course", 
    "Chapter",
    "UserProgress",
    "QuizAnswer",
    "Certificate"
]