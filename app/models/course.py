from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
from app.db.session import Base


class Course(Base):
    __tablename__ = "courses"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - use string references
    chapters: Mapped[List["Chapter"]] = relationship("Chapter", back_populates="course", cascade="all, delete-orphan") #type:ignore
    progress: Mapped[List["UserProgress"]] = relationship("UserProgress", back_populates="course", cascade="all, delete-orphan") #type:ignore