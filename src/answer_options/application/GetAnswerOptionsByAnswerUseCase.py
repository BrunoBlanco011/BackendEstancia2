from typing import List
from src.answer_options.domain.IAnswerOptionRepository import IAnswerOptionRepository
from src.answer_options.domain.entities.AnswerOption import AnswerOption


class GetAnswerOptionsByAnswerUseCase:
    def __init__(self, repository: IAnswerOptionRepository):
        self.repository = repository

    async def execute(self, answer_id: int) -> List[AnswerOption]:
        if answer_id < 1:
            raise ValueError("El ID de la respuesta debe ser mayor a 0")

        return await self.repository.get_by_answer(answer_id)