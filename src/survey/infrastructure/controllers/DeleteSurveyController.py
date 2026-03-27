from fastapi import status
from fastapi.responses import JSONResponse
from src.survey.application.DeleteSurveyUseCase import DeleteSurveyUseCase
from src.survey.domain.dto.SurveyResponse import MessageResponse


class DeleteSurveyController:
    def __init__(self, delete_survey: DeleteSurveyUseCase):
        self.delete_survey = delete_survey

    async def execute(self, survey_id: int):
        try:
            await self.delete_survey.execute(survey_id)

            response = MessageResponse(message="Encuesta eliminada exitosamente")

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
            print(f"Error al eliminar encuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )