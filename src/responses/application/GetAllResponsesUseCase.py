from typing import List
from src.responses.domain.IResponseRepository import IResponseRepository
from src.responses.domain.entities.Response import Response


class GetAllResponsesUseCase:
    def __init__(self, repository: IResponseRepository):
        self.repository = repository

    async def execute(self) -> List[Response]:
        return await self.repository.get_all()