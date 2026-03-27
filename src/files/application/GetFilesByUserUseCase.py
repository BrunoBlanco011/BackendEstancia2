from typing import List
from src.files.domain.IFileRepository import IFileRepository
from src.files.domain.entities.File import File


class GetFilesByUserUseCase:
    def __init__(self, repository: IFileRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> List[File]:
        if user_id < 1:
            raise ValueError("El ID del usuario debe ser mayor a 0")

        return await self.repository.get_by_user(user_id)