from datetime import datetime
from typing import Optional

class Question:
    def __init__(
        self,
        survey_id: int,
        question_text: str,
        question_type: str,
        order_position: int,
        question_id: Optional[int] = None,
        is_required: bool = False,
        created_at: Optional[datetime] = None
    ):
        self.question_id = question_id
        self.survey_id = survey_id
        self.question_text = question_text
        self.question_type = question_type  # 'text', 'multiple', 'checkbox', 'radio', 'scale'
        self.is_required = is_required
        self.order_position = order_position
        self.created_at = created_at