from fastapi import status
from fastapi.responses import JSONResponse
from src.survey.application.GetAllSurveysUseCase import GetAllSurveysUseCase
from src.survey.domain.dto.SurveyResponse import SurveyListResponse, SurveyResponse


class GetAllSurveysController:
    def __init__(self, get_all_surveys: GetAllSurveysUseCase):
        self.get_all_surveys = get_all_surveys

    async def execute(self):
        try:
            surveys = await self.get_all_surveys.execute()

            survey_responses = [SurveyResponse.from_survey(survey) for survey in surveys]

            response = SurveyListResponse(
                surveys=survey_responses,
                total=len(survey_responses)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except Exception as error:
            print(f"Error al obtener encuestas: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )