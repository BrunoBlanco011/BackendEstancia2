from datetime import datetime
from typing import Optional

class QuestionOption:
    def __init__(
        self,
        question_id: int,
        option_text: str,
        order_position: int,
        option_id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self.option_id = option_id
        self.question_id = question_id
        self.option_text = option_text
        self.order_position = order_position
        self.created_at = created_at