from datetime import datetime
from typing import Optional

class AnswerOption:
    def __init__(
        self,
        answer_id: int,
        option_id: int,
        answer_option_id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self.answer_option_id = answer_option_id
        self.answer_id = answer_id
        self.option_id = option_id
        self.created_at = created_at