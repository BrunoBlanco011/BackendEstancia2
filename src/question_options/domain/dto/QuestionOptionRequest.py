from pydantic import BaseModel, Field
from typing import Optional

class CreateQuestionOptionRequest(BaseModel):
    question_id: int = Field(..., ge=1, alias="questionId")
    option_text: str = Field(..., min_length=1, max_length=255, alias="optionText")
    order_position: int = Field(..., ge=1, alias="orderPosition")

    class Config:
        populate_by_name = True


class UpdateQuestionOptionRequest(BaseModel):
    option_text: Optional[str] = Field(None, min_length=1, max_length=255, alias="optionText")
    order_position: Optional[int] = Field(None, ge=1, alias="orderPosition")

    class Config:
        populate_by_name = True