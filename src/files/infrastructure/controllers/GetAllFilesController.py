from fastapi import status
from fastapi.responses import JSONResponse
from src.files.application.GetAllFilesUseCase import GetAllFilesUseCase
from src.files.domain.dto.FileResponse import FileListResponse, FileResponse


class GetAllFilesController:
    def __init__(self, get_all_files: GetAllFilesUseCase):
        self.get_all_files = get_all_files

    async def execute(self):
        try:
            files = await self.get_all_files.execute()

            file_responses = [FileResponse.from_file(file) for file in files]

            response = FileListResponse(
                files=file_responses,
                total=len(file_responses)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except Exception as error:
            print(f"Error al obtener archivos: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )