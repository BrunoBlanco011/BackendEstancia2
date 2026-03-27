from fastapi import status
from fastapi.responses import JSONResponse
from src.survey.application.GetSurveyByIdUseCase import GetSurveyByIdUseCase
from src.survey.domain.dto.SurveyResponse import SingleSurveyResponse, SurveyResponse


class GetSurveyByIdController:
    def __init__(self, get_survey_by_id: GetSurveyByIdUseCase):
        self.get_survey_by_id = get_survey_by_id

    async def execute(self, survey_id: int):
        try:
            survey = await self.get_survey_by_id.execute(survey_id)

            survey_response = SurveyResponse.from_survey(survey)

            response = SingleSurveyResponse(survey=survey_response)

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
            print(f"Error al obtener encuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )