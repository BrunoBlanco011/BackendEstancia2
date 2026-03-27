from typing import Optional
from src.answer_options.domain.IAnswerOptionRepository import IAnswerOptionRepository
from src.answer_options.domain.entities.AnswerOption import AnswerOption


class GetAnswerOptionByIdUseCase:
    def __init__(self, repository: IAnswerOptionRepository):
        self.repository = repository

    async def execute(self, answer_option_id: int) -> Optional[AnswerOption]:
        if answer_option_id < 1:
            raise ValueError("El ID de la opción de respuesta debe ser mayor a 0")

        answer_option = await self.repository.get_by_id(answer_option_id)

        if not answer_option:
            raise ValueError("Opción de respuesta no encontrada")

        return answer_option