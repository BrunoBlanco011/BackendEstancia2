from src.question_options.domain.IQuestionOptionRepository import IQuestionOptionRepository
from src.question_options.domain.entities.QuestionOption import QuestionOption


class UpdateQuestionOptionUseCase:
    def __init__(self, repository: IQuestionOptionRepository):
        self.repository = repository

    async def execute(self, option: QuestionOption) -> None:
        if not option.option_id or option.option_id < 1:
            raise ValueError("El ID de la opción es obligatorio")

        existing_option = await self.repository.get_by_id(option.option_id)
        if not existing_option:
            raise ValueError("Opción no encontrada")

        if option.option_text and len(option.option_text.strip()) > 255:
            raise ValueError("El texto de la opción no puede exceder 255 caracteres")

        if option.order_position and option.order_position < 1:
            raise ValueError("La posición de la opción debe ser mayor a 0")

        await self.repository.update(option)