from typing import Optional
from src.questions.domain.IQuestionRepository import IQuestionRepository
from src.questions.domain.entities.Question import Question


class GetQuestionByIdUseCase:
    def __init__(self, repository: IQuestionRepository):
        self.repository = repository

    async def execute(self, question_id: int) -> Optional[Question]:
        if question_id < 1:
            raise ValueError("El ID de la pregunta debe ser mayor a 0")

        question = await self.repository.get_by_id(question_id)

        if not question:
            raise ValueError("Pregunta no encontrada")

        return question