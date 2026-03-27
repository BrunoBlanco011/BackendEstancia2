from fastapi import status
from fastapi.responses import JSONResponse
from src.questions.application.DeleteQuestionUseCase import DeleteQuestionUseCase
from src.questions.domain.dto.QuestionResponse import MessageResponse

class DeleteQuestionController:
    def __init__(self, delete_question: DeleteQuestionUseCase):
        self.delete_question = delete_question

    async def execute(self, question_id: int):
        try:
            await self.delete_question.execute(question_id)

            response = MessageResponse(message="Pregunta eliminada exitosamente")

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
            print(f"Error al eliminar pregunta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )