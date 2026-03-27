from fastapi import status
from fastapi.responses import JSONResponse
from src.survey.application.UpdateSurveyUseCase import UpdateSurveyUseCase
from src.survey.application.GetSurveyByIdUseCase import GetSurveyByIdUseCase
from src.survey.domain.entities.Survey import Survey
from src.survey.domain.dto.SurveyRequest import UpdateSurveyRequest
from src.survey.domain.dto.SurveyResponse import MessageResponse


class UpdateSurveyController:
    def __init__(
        self,
        update_survey: UpdateSurveyUseCase,
        get_survey_by_id: GetSurveyByIdUseCase
    ):
        self.update_survey = update_survey
        self.get_survey_by_id = get_survey_by_id

    async def execute(self, survey_id: int, request: UpdateSurveyRequest):
        try:
            existing_survey = await self.get_survey_by_id.execute(survey_id)

            if request.name_survey is not None:
                existing_survey.name_survey = request.name_survey
            if request.description is not None:
                existing_survey.description = request.description
            if request.is_active is not None:
                existing_survey.is_active = request.is_active

            await self.update_survey.execute(existing_survey)

            response = MessageResponse(message="Encuesta actualizada exitosamente")

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
            print(f"Error al actualizar encuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )