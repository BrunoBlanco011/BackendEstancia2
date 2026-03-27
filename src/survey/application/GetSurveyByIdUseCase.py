from typing import Optional
from src.survey.domain.ISurveyRepository import ISurveyRepository
from src.survey.domain.entities.Survey import Survey


class GetSurveyByIdUseCase:
    def __init__(self, repository: ISurveyRepository):
        self.repository = repository

    async def execute(self, survey_id: int) -> Optional[Survey]:
        if survey_id < 1:
            raise ValueError("El ID de la encuesta debe ser mayor a 0")

        survey = await self.repository.get_by_id(survey_id)

        if not survey:
            raise ValueError("Encuesta no encontrada")

        return survey