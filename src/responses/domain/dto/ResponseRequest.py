from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class CreateResponseRequest(BaseModel):
    survey_id: int = Field(..., ge=1, alias="surveyId")
    respondent_email: Optional[EmailStr] = Field(None, alias="respondentEmail")
    respondent_user_id: Optional[int] = Field(None, ge=1, alias="respondentUserId")
    ip_address: Optional[str] = Field(None, max_length=45, alias="ipAddress")

    class Config:
        populate_by_name = True