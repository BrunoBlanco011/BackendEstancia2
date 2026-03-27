from typing import List
from src.answers.domain.IAnswerRepository import IAnswerRepository
from src.answers.domain.entities.Answer import Answer


class GetAnswersByQuestionUseCase:
    def __init__(self, repository: IAnswerRepository):
        self.repository = repository

    async def execute(self, question_id: int) -> List[Answer]:
        if question_id < 1:
            raise ValueError("El ID de la pregunta debe ser mayor a 0")

        return await self.repository.get_by_question(question_id)