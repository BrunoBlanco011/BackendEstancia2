from fastapi import status
from fastapi.responses import JSONResponse
from src.responses.application.GetResponsesBySurveyUseCase import GetResponsesBySurveyUseCase
from src.responses.domain.dto.ResponseResponse import ResponseListResponse, ResponseResponse


class GetResponsesBySurveyController:
    def __init__(self, get_responses_by_survey: GetResponsesBySurveyUseCase):
        self.get_responses_by_survey = get_responses_by_survey

    async def execute(self, survey_id: int):
        try:
            responses = await self.get_responses_by_survey.execute(survey_id)

            response_responses = [ResponseResponse.from_response(response) for response in responses]

            response = ResponseListResponse(
                responses=response_responses,
                total=len(response_responses)
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
            print(f"Error al obtener respuestas de la encuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )