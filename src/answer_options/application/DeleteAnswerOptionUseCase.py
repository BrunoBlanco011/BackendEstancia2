from src.answer_options.domain.IAnswerOptionRepository import IAnswerOptionRepository


class DeleteAnswerOptionUseCase:
    def __init__(self, repository: IAnswerOptionRepository):
        self.repository = repository

    async def execute(self, answer_option_id: int) -> None:
        if answer_option_id < 1:
            raise ValueError("El ID de la opción de respuesta debe ser mayor a 0")

        existing_answer_option = await self.repository.get_by_id(answer_option_id)
        if not existing_answer_option:
            raise ValueError("Opción de respuesta no encontrada")

        await self.repository.delete(answer_option_id)