from src.files.domain.IFileRepository import IFileRepository


class DeleteFileUseCase:
    def __init__(self, repository: IFileRepository):
        self.repository = repository

    async def execute(self, file_id: int) -> None:
        if file_id < 1:
            raise ValueError("El ID del archivo debe ser mayor a 0")

        existing_file = await self.repository.get_by_id(file_id)
        if not existing_file:
            raise ValueError("Archivo no encontrado")

        await self.repository.delete(file_id)