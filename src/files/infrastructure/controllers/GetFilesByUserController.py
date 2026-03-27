from fastapi import status
from fastapi.responses import JSONResponse
from src.files.application.GetFilesByUserUseCase import GetFilesByUserUseCase
from src.files.domain.dto.FileResponse import FileListResponse, FileResponse


class GetFilesByUserController:
    def __init__(self, get_files_by_user: GetFilesByUserUseCase):
        self.get_files_by_user = get_files_by_user

    async def execute(self, user_id: int):
        try:
            files = await self.get_files_by_user.execute(user_id)

            file_responses = [FileResponse.from_file(file) for file in files]

            response = FileListResponse(
                files=file_responses,
                total=len(file_responses)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except ValueError as error:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": str(error)}
            )
        except Exception as error:
            print(f"Error al obtener archivos del usuario: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )