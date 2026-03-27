from pydantic import BaseModel
from typing import Optional, List

class QuestionOptionResponse(BaseModel):
    id: Optional[int]
    question_id: int
    option_text: str
    order_position: int
    created_at: str

    @staticmethod
    def from_question_option(option):
        return QuestionOptionResponse(
            id=option.option_id,
            question_id=option.question_id,
            option_text=option.option_text,
            order_position=option.order_position,
            created_at=option.created_at.isoformat() if option.created_at else ""
        )


class QuestionOptionListResponse(BaseModel):
    options: List[QuestionOptionResponse]
    total: int


class SingleQuestionOptionResponse(BaseModel):
    option: QuestionOptionResponse


class CreatedQuestionOptionData(BaseModel):
    optionId: Optional[int]
    questionId: int
    optionText: str
    orderPosition: int
    createdAt: str


class CreateQuestionOptionResponse(BaseModel):
    message: str
    option: CreatedQuestionOptionData


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str