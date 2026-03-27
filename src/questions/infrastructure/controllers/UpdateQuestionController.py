from fastapi import status
from fastapi.responses import JSONResponse
from src.questions.application.UpdateQuestionUseCase import UpdateQuestionUseCase
from src.questions.application.GetQuestionByIdUseCase import GetQuestionByIdUseCase
from src.questions.domain.entities.Question import Question
from src.questions.domain.dto.QuestionRequest import UpdateQuestionRequest
from src.questions.domain.dto.QuestionResponse import MessageResponse

class UpdateQuestionController:
    def __init__(
        self,
        update_question: UpdateQuestionUseCase,
        get_question_by_id: GetQuestionByIdUseCase
    ):
        self.update_question = update_question
        self.get_question_by_id = get_question_by_id

    async def execute(self, question_id: int, request: UpdateQuestionRequest):
        try:
            existing_question = await self.get_question_by_id.execute(question_id)

            if request.question_text is not None:
                existing_question.question_text = request.question_text
            if request.question_type is not None:
                existing_question.question_type = request.question_type
            if request.is_required is not None:
                existing_question.is_required = request.is_required
            if request.order_position is not None:
                existing_question.order_position = request.order_position

            await self.update_question.execute(existing_question)

            response = MessageResponse(message="Pregunta actualizada exitosamente")

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
            print(f"Error al actualizar pregunta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )