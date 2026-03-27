from src.questions.domain.IQuestionRepository import IQuestionRepository
from src.questions.domain.entities.Question import Question


class UpdateQuestionUseCase:
    def __init__(self, repository: IQuestionRepository):
        self.repository = repository

    async def execute(self, question: Question) -> None:
        if not question.question_id or question.question_id < 1:
            raise ValueError("El ID de la pregunta es obligatorio")

        existing_question = await self.repository.get_by_id(question.question_id)
        if not existing_question:
            raise ValueError("Pregunta no encontrada")

        if question.question_type:
            valid_types = ['text', 'multiple', 'checkbox', 'radio', 'scale']
            if question.question_type not in valid_types:
                raise ValueError(f"Tipo de pregunta inválido. Debe ser uno de: {', '.join(valid_types)}")

        if question.order_position and question.order_position < 1:
            raise ValueError("La posición de la pregunta debe ser mayor a 0")

        await self.repository.update(question)