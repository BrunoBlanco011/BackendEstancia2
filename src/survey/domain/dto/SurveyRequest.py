from pydantic import BaseModel, Field
from typing import Optional

class CreateSurveyRequest(BaseModel):
    name_survey: str = Field(..., min_length=1, max_length=100, alias="nameSurvey")
    description: str = Field(..., min_length=1, max_length=80)
    created_by: int = Field(..., ge=1, alias="createdBy")

    class Config:
        populate_by_name = True


class UpdateSurveyRequest(BaseModel):
    name_survey: Optional[str] = Field(None, min_length=1, max_length=100, alias="nameSurvey")
    description: Optional[str] = Field(None, min_length=1, max_length=80)
    is_active: Optional[bool] = Field(None, alias="isActive")

    class Config:
        populate_by_name = True