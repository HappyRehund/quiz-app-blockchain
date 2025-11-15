from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
from app.db.session import Base


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
    
    # Relationships - use string references
    course: Mapped["Course"] = relationship("Course", back_populates="chapters") # type:ignore
    quiz_answers: Mapped[List["QuizAnswer"]] = relationship("QuizAnswer", back_populates="chapter", cascade="all, delete-orphan") # type:ignore