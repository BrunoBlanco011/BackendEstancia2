from typing import List
from src.question_options.domain.IQuestionOptionRepository import IQuestionOptionRepository
from src.question_options.domain.entities.QuestionOption import QuestionOption


class GetOptionsByQuestionUseCase:
    def __init__(self, repository: IQuestionOptionRepository):
        self.repository = repository

    async def execute(self, question_id: int) -> List[QuestionOption]:
        if question_id < 1:
            raise ValueError("El ID de la pregunta debe ser mayor a 0")

        return await self.repository.get_by_question(question_id)