from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class Chapter(Base):
    __tablename__ = "chapters"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    quiz_question = Column(Text, nullable=False)
    quiz_options = Column(Text, nullable=False)  # JSON string format: ["opt1", "opt2", "opt3", "opt4"]
    quiz_correct_answer = Column(Integer, nullable=False)  # Index of correct answer (0-3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="chapters")
    quiz_answers = relationship("QuizAnswer", back_populates="chapter", cascade="all, delete-orphan")