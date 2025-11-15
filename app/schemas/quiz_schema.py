from pydantic import BaseModel


class QuizSubmit(BaseModel):
    chapter_id: int
    answer_index: int


class QuizResult(BaseModel):
    is_correct: bool
    correct_answer_index: int
    message: str