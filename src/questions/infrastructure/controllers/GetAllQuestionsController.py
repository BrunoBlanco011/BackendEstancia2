from fastapi import status
from fastapi.responses import JSONResponse
from src.questions.application.GetAllQuestionsUseCase import GetAllQuestionsUseCase
from src.questions.domain.dto.QuestionResponse import QuestionListResponse, QuestionResponse

class GetAllQuestionsController:
    def __init__(self, get_all_questions: GetAllQuestionsUseCase):
        self.get_all_questions = get_all_questions

    async def execute(self):
        try:
            questions = await self.get_all_questions.execute()

            question_responses = [QuestionResponse.from_question(question) for question in questions]

            response = QuestionListResponse(
                questions=question_responses,
                total=len(question_responses)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except Exception as error:
            print(f"Error al obtener preguntas: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )