from fastapi import status
from fastapi.responses import JSONResponse
from src.answer_options.application.DeleteAnswerOptionUseCase import DeleteAnswerOptionUseCase
from src.answer_options.domain.dto.AnswerOptionResponse import MessageResponse


class DeleteAnswerOptionController:
    def __init__(self, delete_answer_option: DeleteAnswerOptionUseCase):
        self.delete_answer_option = delete_answer_option

    async def execute(self, answer_option_id: int):
        try:
            await self.delete_answer_option.execute(answer_option_id)

            response = MessageResponse(message="Opción de respuesta eliminada exitosamente")

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
            print(f"Error al eliminar opción de respuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )