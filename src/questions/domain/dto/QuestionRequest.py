from pydantic import BaseModel, Field
from typing import Optional

class CreateQuestionRequest(BaseModel):
    survey_id: int = Field(..., ge=1, alias="surveyId")
    question_text: str = Field(..., min_length=1, alias="questionText")
    question_type: str = Field(..., pattern="^(text|multiple|checkbox|radio|scale)$", alias="questionType")
    is_required: bool = Field(False, alias="isRequired")
    order_position: int = Field(..., ge=1, alias="orderPosition")

    class Config:
        populate_by_name = True


class UpdateQuestionRequest(BaseModel):
    question_text: Optional[str] = Field(None, min_length=1, alias="questionText")
    question_type: Optional[str] = Field(None, pattern="^(text|multiple|checkbox|radio|scale)$", alias="questionType")
    is_required: Optional[bool] = Field(None, alias="isRequired")
    order_position: Optional[int] = Field(None, ge=1, alias="orderPosition")

    class Config:
        populate_by_name = True