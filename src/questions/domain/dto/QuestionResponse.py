from pydantic import BaseModel
from typing import Optional, List

class QuestionResponse(BaseModel):
    id: Optional[int]
    survey_id: int
    question_text: str
    question_type: str
    is_required: bool
    order_position: int
    created_at: str

    @staticmethod
    def from_question(question):
        return QuestionResponse(
            id=question.question_id,
            survey_id=question.survey_id,
            question_text=question.question_text,
            question_type=question.question_type,
            is_required=question.is_required,
            order_position=question.order_position,
            created_at=question.created_at.isoformat() if question.created_at else ""
        )


class QuestionListResponse(BaseModel):
    questions: List[QuestionResponse]
    total: int


class SingleQuestionResponse(BaseModel):
    question: QuestionResponse


class CreatedQuestionData(BaseModel):
    questionId: Optional[int]
    surveyId: int
    questionText: str
    questionType: str
    isRequired: bool
    orderPosition: int
    createdAt: str


class CreateQuestionResponse(BaseModel):
    message: str
    question: CreatedQuestionData


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str