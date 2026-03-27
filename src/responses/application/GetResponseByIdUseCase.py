from typing import Optional
from src.responses.domain.IResponseRepository import IResponseRepository
from src.responses.domain.entities.Response import Response


class GetResponseByIdUseCase:
    def __init__(self, repository: IResponseRepository):
        self.repository = repository

    async def execute(self, response_id: int) -> Optional[Response]:
        if response_id < 1:
            raise ValueError("El ID de la respuesta debe ser mayor a 0")

        response = await self.repository.get_by_id(response_id)

        if not response:
            raise ValueError("Respuesta no encontrada")

        return response