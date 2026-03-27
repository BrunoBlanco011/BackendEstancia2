from pydantic import BaseModel, Field, validator
from typing import Optional

class CreateAnswerRequest(BaseModel):
    response_id: int = Field(..., ge=1, alias="responseId")
    question_id: int = Field(..., ge=1, alias="questionId")
    answer_text: Optional[str] = Field(None, alias="answerText")
    selected_option_id: Optional[int] = Field(None, ge=1, alias="selectedOptionId")
    scale_value: Optional[int] = Field(None, ge=1, le=5, alias="scaleValue")

    @validator('scale_value')
    def validate_scale(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('El valor de escala debe estar entre 1 y 5')
        return v

    class Config:
        populate_by_name = True


class UpdateAnswerRequest(BaseModel):
    answer_text: Optional[str] = Field(None, alias="answerText")
    selected_option_id: Optional[int] = Field(None, ge=1, alias="selectedOptionId")
    scale_value: Optional[int] = Field(None, ge=1, le=5, alias="scaleValue")

    @validator('scale_value')
    def validate_scale(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('El valor de escala debe estar entre 1 y 5')
        return v

    class Config:
        populate_by_name = True