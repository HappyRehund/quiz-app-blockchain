from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ChapterBase(BaseModel):
    title: str
    content: str
    quiz_question: str


class ChapterCreate(ChapterBase):
    course_id: int
    chapter_number: int
    quiz_options: List[str]
    quiz_correct_answer: int


class ChapterResponse(BaseModel):
    id: int
    course_id: int
    chapter_number: int
    title: str
    content: str
    quiz_question: str
    quiz_options: List[str]
    is_completed: bool = False
    
    class Config:
        from_attributes = True


class ChapterListResponse(BaseModel):
    id: int
    chapter_number: int
    title: str
    is_completed: bool = False
    
    class Config:
        from_attributes = True