from fastapi import status
from fastapi.responses import JSONResponse
from src.survey.application.CreateSurveyUseCase import CreateSurveyUseCase
from src.survey.domain.entities.Survey import Survey
from src.survey.domain.dto.SurveyRequest import CreateSurveyRequest
from src.survey.domain.dto.SurveyResponse import CreateSurveyResponse, CreatedSurveyData
from datetime import datetime


class CreateSurveyController:
    def __init__(self, create_survey: CreateSurveyUseCase):
        self.create_survey = create_survey

    async def execute(self, request: CreateSurveyRequest):
        try:
            survey = Survey(
                name_survey=request.name_survey,
                description=request.description,
                created_by=request.created_by
            )

            saved_survey = await self.create_survey.execute(survey)

            response = CreateSurveyResponse(
                message="Encuesta creada exitosamente",
                survey=CreatedSurveyData(
                    surveyId=saved_survey.survey_id,
                    nameSurvey=saved_survey.name_survey,
                    description=saved_survey.description,
                    createdBy=saved_survey.created_by,
                    createdAt=saved_survey.created_at.isoformat(),
                    isActive=saved_survey.is_active
                )
            )

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=response.model_dump()
            )

        except ValueError as error:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": str(error)}
            )
        except Exception as error:
            print(f"Error al crear encuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )