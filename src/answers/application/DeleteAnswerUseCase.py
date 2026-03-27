from src.answers.domain.IAnswerRepository import IAnswerRepository


class DeleteAnswerUseCase:
    def __init__(self, repository: IAnswerRepository):
        self.repository = repository

    async def execute(self, answer_id: int) -> None:
        if answer_id < 1:
            raise ValueError("El ID de la respuesta debe ser mayor a 0")

        existing_answer = await self.repository.get_by_id(answer_id)
        if not existing_answer:
            raise ValueError("Respuesta no encontrada")

        await self.repository.delete(answer_id)