from typing import List
from src.answers.domain.IAnswerRepository import IAnswerRepository
from src.answers.domain.entities.Answer import Answer


class GetAnswersByResponseUseCase:
    def __init__(self, repository: IAnswerRepository):
        self.repository = repository

    async def execute(self, response_id: int) -> List[Answer]:
        if response_id < 1:
            raise ValueError("El ID de la respuesta debe ser mayor a 0")

        return await self.repository.get_by_response(response_id)