from datetime import datetime
from typing import Optional

class Response:
    def __init__(
        self,
        survey_id: int,
        response_id: Optional[int] = None,
        respondent_email: Optional[str] = None,
        respondent_user_id: Optional[int] = None,
        submitted_at: Optional[datetime] = None,
        ip_address: Optional[str] = None
    ):
        self.response_id = response_id
        self.survey_id = survey_id
        self.respondent_email = respondent_email
        self.respondent_user_id = respondent_user_id
        self.submitted_at = submitted_at
        self.ip_address = ip_address