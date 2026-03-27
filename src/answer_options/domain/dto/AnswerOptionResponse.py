from pydantic import BaseModel
from typing import Optional, List

class AnswerOptionResponse(BaseModel):
    id: Optional[int]
    answer_id: int
    option_id: int
    created_at: str

    @staticmethod
    def from_answer_option(answer_option):
        return AnswerOptionResponse(
            id=answer_option.answer_option_id,
            answer_id=answer_option.answer_id,
            option_id=answer_option.option_id,
            created_at=answer_option.created_at.isoformat() if answer_option.created_at else ""
        )


class AnswerOptionListResponse(BaseModel):
    answer_options: List[AnswerOptionResponse]
    total: int


class SingleAnswerOptionResponse(BaseModel):
    answer_option: AnswerOptionResponse


class CreatedAnswerOptionData(BaseModel):
    answerOptionId: Optional[int]
    answerId: int
    optionId: int
    createdAt: str


class CreateAnswerOptionResponse(BaseModel):
    message: str
    answer_option: CreatedAnswerOptionData


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str