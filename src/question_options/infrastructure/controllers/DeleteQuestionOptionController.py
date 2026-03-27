from fastapi import status
from fastapi.responses import JSONResponse
from src.question_options.application.DeleteQuestionOptionUseCase import DeleteQuestionOptionUseCase
from src.question_options.domain.dto.QuestionOptionResponse import MessageResponse


class DeleteQuestionOptionController:
    def __init__(self, delete_option: DeleteQuestionOptionUseCase):
        self.delete_option = delete_option

    async def execute(self, option_id: int):
        try:
            await self.delete_option.execute(option_id)

            response = MessageResponse(message="Opción eliminada exitosamente")

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
            print(f"Error al eliminar opción: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )