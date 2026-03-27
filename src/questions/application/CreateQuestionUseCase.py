from src.questions.domain.IQuestionRepository import IQuestionRepository
from src.questions.domain.entities.Question import Question


class CreateQuestionUseCase:
    def __init__(self, repository: IQuestionRepository):
        self.repository = repository

    async def execute(self, question: Question) -> Question:
        if not question.survey_id or question.survey_id < 1:
            raise ValueError("El ID de la encuesta es obligatorio")

        if not question.question_text or not question.question_text.strip():
            raise ValueError("El texto de la pregunta es obligatorio")

        if not question.question_type or not question.question_type.strip():
            raise ValueError("El tipo de pregunta es obligatorio")

        valid_types = ['text', 'multiple', 'checkbox', 'radio', 'scale']
        if question.question_type not in valid_types:
            raise ValueError(f"Tipo de pregunta inválido. Debe ser uno de: {', '.join(valid_types)}")

        if not question.order_position or question.order_position < 1:
            raise ValueError("La posición de la pregunta debe ser mayor a 0")

        return await self.repository.save(question)