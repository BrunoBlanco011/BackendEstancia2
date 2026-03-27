from src.question_options.domain.IQuestionOptionRepository import IQuestionOptionRepository


class DeleteQuestionOptionUseCase:
    def __init__(self, repository: IQuestionOptionRepository):
        self.repository = repository

    async def execute(self, option_id: int) -> None:
        if option_id < 1:
            raise ValueError("El ID de la opción debe ser mayor a 0")

        existing_option = await self.repository.get_by_id(option_id)
        if not existing_option:
            raise ValueError("Opción no encontrada")

        await self.repository.delete(option_id)