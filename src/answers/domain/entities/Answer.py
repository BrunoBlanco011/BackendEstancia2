from datetime import datetime
from typing import Optional

class Answer:
    def __init__(
        self,
        response_id: int,
        question_id: int,
        answer_id: Optional[int] = None,
        answer_text: Optional[str] = None,
        selected_option_id: Optional[int] = None,
        scale_value: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self.answer_id = answer_id
        self.response_id = response_id
        self.question_id = question_id
        self.answer_text = answer_text  # Para preguntas tipo 'text'
        self.selected_option_id = selected_option_id  # Para 'radio', 'multiple'
        self.scale_value = scale_value  # Para 'scale'
        self.created_at = created_at