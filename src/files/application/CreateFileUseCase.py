from src.files.domain.IFileRepository import IFileRepository
from src.files.domain.entities.File import File


class CreateFileUseCase:
    def __init__(self, repository: IFileRepository):
        self.repository = repository

    async def execute(self, file: File) -> File:
        if not file.file_name or not file.file_name.strip():
            raise ValueError("El nombre del archivo es obligatorio")

        if not file.original_name or not file.original_name.strip():
            raise ValueError("El nombre original del archivo es obligatorio")

        if not file.file_path or not file.file_path.strip():
            raise ValueError("La ruta del archivo es obligatoria")

        if not file.file_size or file.file_size < 1:
            raise ValueError("El tamaño del archivo debe ser mayor a 0")

        if not file.file_type or not file.file_type.strip():
            raise ValueError("El tipo de archivo es obligatorio")

        valid_types = ['csv', 'xlsx', 'xls', 'xlsm']
        if file.file_type.lower() not in valid_types:
            raise ValueError(f"Tipo de archivo no permitido. Debe ser uno de: {', '.join(valid_types)}")

        if not file.uploaded_by or file.uploaded_by < 1:
            raise ValueError("El ID del usuario que sube el archivo es obligatorio")

        return await self.repository.save(file)