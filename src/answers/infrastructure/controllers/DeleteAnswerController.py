from fastapi import status
from fastapi.responses import JSONResponse
from src.answers.application.DeleteAnswerUseCase import DeleteAnswerUseCase
from src.answers.domain.dto.AnswerResponse import MessageResponse


class DeleteAnswerController:
    def __init__(self, delete_answer: DeleteAnswerUseCase):
        self.delete_answer = delete_answer

    async def execute(self, answer_id: int):
        try:
            await self.delete_answer.execute(answer_id)

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