from typing import List
from src.answers.domain.IAnswerRepository import IAnswerRepository
from src.answers.domain.entities.Answer import Answer


class GetAllAnswersUseCase:
    def __init__(self, repository: IAnswerRepository):
        self.repository = repository

    async def execute(self) -> List[Answer]:
        return await self.repository.get_all()