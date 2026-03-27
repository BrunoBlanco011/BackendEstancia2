from src.responses.domain.IResponseRepository import IResponseRepository


class DeleteResponseUseCase:
    def __init__(self, repository: IResponseRepository):
        self.repository = repository

    async def execute(self, response_id: int) -> None:
        if response_id < 1:
            raise ValueError("El ID de la respuesta debe ser mayor a 0")

        existing_response = await self.repository.get_by_id(response_id)
        if not existing_response:
            raise ValueError("Respuesta no encontrada")

        await self.repository.delete(response_id)