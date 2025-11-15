from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, TYPE_CHECKING
from app.db.session import Base

if TYPE_CHECKING:
    from app.models.chapter import Chapter
    from app.models.user_progress import UserProgress


class Course(Base):
    __tablename__ = "courses"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chapters: Mapped[List["Chapter"]] = relationship(back_populates="course", cascade="all, delete-orphan")
    progress: Mapped[List["UserProgress"]] = relationship(back_populates="course", cascade="all, delete-orphan")