from pydantic import BaseModel
from typing import Optional, List

class AnswerResponse(BaseModel):
    id: Optional[int]
    response_id: int
    question_id: int
    answer_text: Optional[str]
    selected_option_id: Optional[int]
    scale_value: Optional[int]
    created_at: str

    @staticmethod
    def from_answer(answer):
        return AnswerResponse(
            id=answer.answer_id,
            response_id=answer.response_id,
            question_id=answer.question_id,
            answer_text=answer.answer_text,
            selected_option_id=answer.selected_option_id,
            scale_value=answer.scale_value,
            created_at=answer.created_at.isoformat() if answer.created_at else ""
        )


class AnswerListResponse(BaseModel):
    answers: List[AnswerResponse]
    total: int


class SingleAnswerResponse(BaseModel):
    answer: AnswerResponse


class CreatedAnswerData(BaseModel):
    answerId: Optional[int]
    responseId: int
    questionId: int
    answerText: Optional[str]
    selectedOptionId: Optional[int]
    scaleValue: Optional[int]
    createdAt: str


class CreateAnswerResponse(BaseModel):
    message: str
    answer: CreatedAnswerData


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str