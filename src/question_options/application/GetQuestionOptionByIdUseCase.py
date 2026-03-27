from typing import Optional
from src.question_options.domain.IQuestionOptionRepository import IQuestionOptionRepository
from src.question_options.domain.entities.QuestionOption import QuestionOption


class GetQuestionOptionByIdUseCase:
    def __init__(self, repository: IQuestionOptionRepository):
        self.repository = repository

    async def execute(self, option_id: int) -> Optional[QuestionOption]:
        if option_id < 1:
            raise ValueError("El ID de la opción debe ser mayor a 0")

        option = await self.repository.get_by_id(option_id)

        if not option:
            raise ValueError("Opción no encontrada")

        return option