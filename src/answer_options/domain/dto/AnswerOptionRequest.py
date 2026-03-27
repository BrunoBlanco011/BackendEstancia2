from pydantic import BaseModel, Field

class CreateAnswerOptionRequest(BaseModel):
    answer_id: int = Field(..., ge=1, alias="answerId")
    option_id: int = Field(..., ge=1, alias="optionId")

    class Config:
        populate_by_name = True