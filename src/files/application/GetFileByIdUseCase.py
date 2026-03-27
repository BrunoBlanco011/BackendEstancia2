from typing import Optional
from src.files.domain.IFileRepository import IFileRepository
from src.files.domain.entities.File import File


class GetFileByIdUseCase:
    def __init__(self, repository: IFileRepository):
        self.repository = repository

    async def execute(self, file_id: int) -> Optional[File]:
        if file_id < 1:
            raise ValueError("El ID del archivo debe ser mayor a 0")

        file = await self.repository.get_by_id(file_id)

        if not file:
            raise ValueError("Archivo no encontrado")

        return file