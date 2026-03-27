from fastapi import status
from fastapi.responses import JSONResponse
from src.survey.application.GetSurveysByUserUseCase import GetSurveysByUserUseCase
from src.survey.domain.dto.SurveyResponse import SurveyListResponse, SurveyResponse


class GetSurveysByUserController:
    def __init__(self, get_surveys_by_user: GetSurveysByUserUseCase):
        self.get_surveys_by_user = get_surveys_by_user

    async def execute(self, user_id: int):
        try:
            surveys = await self.get_surveys_by_user.execute(user_id)

            survey_responses = [SurveyResponse.from_survey(survey) for survey in surveys]

            response = SurveyListResponse(
                surveys=survey_responses,
                total=len(survey_responses)
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
            print(f"Error al obtener encuestas del usuario: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )