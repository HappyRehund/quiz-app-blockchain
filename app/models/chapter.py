from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, TYPE_CHECKING
from app.db.session import Base

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.quiz_answer import QuizAnswer


class Chapter(Base):
    __tablename__ = "chapters"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    chapter_number: Mapped[int]
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    quiz_question: Mapped[str] = mapped_column(Text)
    quiz_options: Mapped[str] = mapped_column(Text)
    quiz_correct_answer: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course: Mapped["Course"] = relationship(back_populates="chapters")
    quiz_answers: Mapped[List["QuizAnswer"]] = relationship(back_populates="chapter", cascade="all, delete-orphan")