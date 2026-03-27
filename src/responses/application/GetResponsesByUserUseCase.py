from typing import List
from src.responses.domain.IResponseRepository import IResponseRepository
from src.responses.domain.entities.Response import Response


class GetResponsesByUserUseCase:
    def __init__(self, repository: IResponseRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> List[Response]:
        if user_id < 1:
            raise ValueError("El ID del usuario debe ser mayor a 0")

        return await self.repository.get_by_user(user_id)