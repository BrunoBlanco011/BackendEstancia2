from typing import List
from src.files.domain.IFileRepository import IFileRepository
from src.files.domain.entities.File import File


class GetAllFilesUseCase:
    def __init__(self, repository: IFileRepository):
        self.repository = repository

    async def execute(self) -> List[File]:
        return await self.repository.get_all()