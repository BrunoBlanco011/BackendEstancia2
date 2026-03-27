from typing import List
from src.question_options.domain.IQuestionOptionRepository import IQuestionOptionRepository
from src.question_options.domain.entities.QuestionOption import QuestionOption


class GetAllQuestionOptionsUseCase:
    def __init__(self, repository: IQuestionOptionRepository):
        self.repository = repository

    async def execute(self) -> List[QuestionOption]:
        return await self.repository.get_all()