from fastapi import status
from fastapi.responses import JSONResponse
from src.files.application.GetFileByIdUseCase import GetFileByIdUseCase
from src.files.domain.dto.FileResponse import SingleFileResponse, FileResponse


class GetFileByIdController:
    def __init__(self, get_file_by_id: GetFileByIdUseCase):
        self.get_file_by_id = get_file_by_id

    async def execute(self, file_id: int):
        try:
            file = await self.get_file_by_id.execute(file_id)

            file_response = FileResponse.from_file(file)

            response = SingleFileResponse(file=file_response)

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
            print(f"Error al obtener archivo: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )