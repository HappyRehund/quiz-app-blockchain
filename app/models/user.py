from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, TYPE_CHECKING
from app.db.session import Base

if TYPE_CHECKING:
    from app.models.user_progress import UserProgress
    from app.models.quiz_answer import QuizAnswer
    from app.models.certificate import Certificate


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    progress: Mapped[List["UserProgress"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    quiz_answers: Mapped[List["QuizAnswer"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    certificates: Mapped[List["Certificate"]] = relationship(back_populates="user", cascade="all, delete-orphan")