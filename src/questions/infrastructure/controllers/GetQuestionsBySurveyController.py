from fastapi import status
from fastapi.responses import JSONResponse
from src.questions.application.GetQuestionsBySurveyUseCase import GetQuestionsBySurveyUseCase
from src.questions.domain.dto.QuestionResponse import QuestionListResponse, QuestionResponse

class GetQuestionsBySurveyController:
    def __init__(self, get_questions_by_survey: GetQuestionsBySurveyUseCase):
        self.get_questions_by_survey = get_questions_by_survey

    async def execute(self, survey_id: int):
        try:
            questions = await self.get_questions_by_survey.execute(survey_id)

            question_responses = [QuestionResponse.from_question(question) for question in questions]

            response = QuestionListResponse(
                questions=question_responses,
                total=len(question_responses)
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
            print(f"Error al obtener preguntas de la encuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )