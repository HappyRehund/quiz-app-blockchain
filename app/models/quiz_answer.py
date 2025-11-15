from sqlalchemy import ForeignKey, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
from app.db.session import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.chapter import Chapter


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
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="quiz_answers")
    chapter: Mapped["Chapter"] = relationship(back_populates="quiz_answers")