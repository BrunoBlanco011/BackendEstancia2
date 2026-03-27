from fastapi import status
from fastapi.responses import JSONResponse
from src.responses.application.DeleteResponseUseCase import DeleteResponseUseCase
from src.responses.domain.dto.ResponseResponse import MessageResponse


class DeleteResponseController:
    def __init__(self, delete_response: DeleteResponseUseCase):
        self.delete_response = delete_response

    async def execute(self, response_id: int):
        try:
            await self.delete_response.execute(response_id)

            response = MessageResponse(message="Respuesta eliminada exitosamente")

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
            print(f"Error al eliminar respuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )