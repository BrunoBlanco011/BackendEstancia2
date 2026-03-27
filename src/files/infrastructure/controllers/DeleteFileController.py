from fastapi import status
from fastapi.responses import JSONResponse
from src.files.application.DeleteFileUseCase import DeleteFileUseCase
from src.files.application.GetFileByIdUseCase import GetFileByIdUseCase
from src.files.domain.dto.FileResponse import MessageResponse
from src.core.cloudinary_service import get_cloudinary_service


class DeleteFileController:
    def __init__(
        self,
        delete_file: DeleteFileUseCase,
        get_file_by_id: GetFileByIdUseCase
    ):
        self.delete_file = delete_file
        self.get_file_by_id = get_file_by_id
        self.cloudinary_service = get_cloudinary_service()

    async def execute(self, file_id: int):
        try:
            file = await self.get_file_by_id.execute(file_id)
            if file.file_name:
                deleted = self.cloudinary_service.delete_file(
                    file.file_name,
                    resource_type="raw"
                )
                if not deleted:
                    print(f"Advertencia: No se pudo eliminar el archivo de Cloudinary: {file.file_name}")

            await self.delete_file.execute(file_id)

            response = MessageResponse(message="Archivo eliminado exitosamente")

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except ValueError as error:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": str(error)}
            )
        except Exception as error:
            print(f"Error al eliminar archivo: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )