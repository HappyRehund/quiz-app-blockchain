from sqlalchemy import ForeignKey, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.session import Base


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapters.id"))
    answer_index: Mapped[int]
    is_correct: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'chapter_id', name='unique_user_chapter_answer'),
    )
    
    # Relationships - use string references
    user: Mapped["User"] = relationship("User", back_populates="quiz_answers") # type:ignore
    chapter: Mapped["Chapter"] = relationship("Chapter", back_populates="quiz_answers") # type:ignore