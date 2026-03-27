from typing import List
from src.questions.domain.IQuestionRepository import IQuestionRepository
from src.questions.domain.entities.Question import Question


class GetAllQuestionsUseCase:
    def __init__(self, repository: IQuestionRepository):
        self.repository = repository

    async def execute(self) -> List[Question]:
        return await self.repository.get_all()