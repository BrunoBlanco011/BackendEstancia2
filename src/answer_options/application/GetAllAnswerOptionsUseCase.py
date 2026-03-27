from typing import List
from src.answer_options.domain.IAnswerOptionRepository import IAnswerOptionRepository
from src.answer_options.domain.entities.AnswerOption import AnswerOption


class GetAllAnswerOptionsUseCase:
    def __init__(self, repository: IAnswerOptionRepository):
        self.repository = repository

    async def execute(self) -> List[AnswerOption]:
        return await self.repository.get_all()