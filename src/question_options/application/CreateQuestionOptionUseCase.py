from src.question_options.domain.IQuestionOptionRepository import IQuestionOptionRepository
from src.question_options.domain.entities.QuestionOption import QuestionOption


class CreateQuestionOptionUseCase:
    def __init__(self, repository: IQuestionOptionRepository):
        self.repository = repository

    async def execute(self, option: QuestionOption) -> QuestionOption:
        if not option.question_id or option.question_id < 1:
            raise ValueError("El ID de la pregunta es obligatorio")

        if not option.option_text or not option.option_text.strip():
            raise ValueError("El texto de la opción es obligatorio")

        if len(option.option_text.strip()) > 255:
            raise ValueError("El texto de la opción no puede exceder 255 caracteres")

        if not option.order_position or option.order_position < 1:
            raise ValueError("La posición de la opción debe ser mayor a 0")

        return await self.repository.save(option)