from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CourseBase(BaseModel):
    title: str
    description: str


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    total_chapters: int = 0
    user_progress: Optional[int] = 0  # chapters completed by current user
    
    class Config:
        from_attributes = True


class CourseListResponse(BaseModel):
    id: int
    title: str
    description: str
    total_chapters: int
    user_progress: int = 0
    
    class Config:
        from_attributes = True