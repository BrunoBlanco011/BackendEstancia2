from typing import Optional
from src.answers.domain.IAnswerRepository import IAnswerRepository
from src.answers.domain.entities.Answer import Answer


class GetAnswerByIdUseCase:
    def __init__(self, repository: IAnswerRepository):
        self.repository = repository

    async def execute(self, answer_id: int) -> Optional[Answer]:
        if answer_id < 1:
            raise ValueError("El ID de la respuesta debe ser mayor a 0")

        answer = await self.repository.get_by_id(answer_id)

        if not answer:
            raise ValueError("Respuesta no encontrada")

        return answer