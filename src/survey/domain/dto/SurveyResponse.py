from pydantic import BaseModel
from typing import Optional, List

class SurveyResponse(BaseModel):
    id: Optional[int]
    name_survey: str
    description: str
    created_by: int
    created_at: str
    updated_at: str
    is_active: bool

    @staticmethod
    def from_survey(survey):
        return SurveyResponse(
            id=survey.survey_id,
            name_survey=survey.name_survey,
            description=survey.description,
            created_by=survey.created_by,
            created_at=survey.created_at.isoformat() if survey.created_at else "",
            updated_at=survey.updated_at.isoformat() if survey.updated_at else "",
            is_active=survey.is_active
        )


class SurveyListResponse(BaseModel):
    surveys: List[SurveyResponse]
    total: int


class SingleSurveyResponse(BaseModel):
    survey: SurveyResponse


class CreatedSurveyData(BaseModel):
    surveyId: Optional[int]
    nameSurvey: str
    description: str
    createdBy: int
    createdAt: str
    isActive: bool


class CreateSurveyResponse(BaseModel):
    message: str
    survey: CreatedSurveyData


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str