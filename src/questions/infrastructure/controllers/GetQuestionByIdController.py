from fastapi import status
from fastapi.responses import JSONResponse
from src.questions.application.GetQuestionByIdUseCase import GetQuestionByIdUseCase
from src.questions.domain.dto.QuestionResponse import SingleQuestionResponse, QuestionResponse

class GetQuestionByIdController:
    def __init__(self, get_question_by_id: GetQuestionByIdUseCase):
        self.get_question_by_id = get_question_by_id

    async def execute(self, question_id: int):
        try:
            question = await self.get_question_by_id.execute(question_id)

            question_response = QuestionResponse.from_question(question)

            response = SingleQuestionResponse(question=question_response)

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
            print(f"Error al obtener pregunta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )