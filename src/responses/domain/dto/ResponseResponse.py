from pydantic import BaseModel
from typing import Optional, List

class ResponseResponse(BaseModel):
    id: Optional[int]
    survey_id: int
    respondent_email: Optional[str]
    respondent_user_id: Optional[int]
    submitted_at: str
    ip_address: Optional[str]

    @staticmethod
    def from_response(response):
        return ResponseResponse(
            id=response.response_id,
            survey_id=response.survey_id,
            respondent_email=response.respondent_email,
            respondent_user_id=response.respondent_user_id,
            submitted_at=response.submitted_at.isoformat() if response.submitted_at else "",
            ip_address=response.ip_address
        )


class ResponseListResponse(BaseModel):
    responses: List[ResponseResponse]
    total: int


class SingleResponseResponse(BaseModel):
    response: ResponseResponse


class CreatedResponseData(BaseModel):
    responseId: Optional[int]
    surveyId: int
    respondentEmail: Optional[str]
    respondentUserId: Optional[int]
    submittedAt: str
    ipAddress: Optional[str]


class CreateResponseResponse(BaseModel):
    message: str
    response: CreatedResponseData


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str