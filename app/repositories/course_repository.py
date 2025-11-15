from sqlalchemy.orm import Session
from app.models.course import Course
from typing import List, Optional


class CourseRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_course(self, title: str, description: str) -> Course:
        """Create a new course"""
        course = Course(title=title, description=description)
        self.db.add(course)
        self.db.flush()
        self.db.refresh(course)
        return course
    
    def get_all_courses(self) -> List[Course]:
        """Get all courses"""
        return self.db.query(Course).all()
    
    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        """Get course by ID"""
        return self.db.query(Course).filter(Course.id == course_id).first()