from src.answer_options.domain.IAnswerOptionRepository import IAnswerOptionRepository
from src.answer_options.domain.entities.AnswerOption import AnswerOption


class CreateAnswerOptionUseCase:
    def __init__(self, repository: IAnswerOptionRepository):
        self.repository = repository

    async def execute(self, answer_option: AnswerOption) -> AnswerOption:
        if not answer_option.answer_id or answer_option.answer_id < 1:
            raise ValueError("El ID de la respuesta es obligatorio")

        if not answer_option.option_id or answer_option.option_id < 1:
            raise ValueError("El ID de la opción es obligatorio")

        return await self.repository.save(answer_option)