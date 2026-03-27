from datetime import datetime
from typing import Optional

class Survey:
    def __init__(
        self,
        name_survey: str,
        description: str,
        created_by: int,
        survey_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        is_active: bool = True
    ):
        self.survey_id = survey_id
        self.name_survey = name_survey
        self.description = description
        self.created_by = created_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active