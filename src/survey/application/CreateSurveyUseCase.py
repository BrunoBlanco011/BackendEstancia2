from src.survey.domain.ISurveyRepository import ISurveyRepository
from src.survey.domain.entities.Survey import Survey


class CreateSurveyUseCase:
    def __init__(self, repository: ISurveyRepository):
        self.repository = repository

    async def execute(self, survey: Survey) -> Survey:
        if not survey.name_survey or not survey.name_survey.strip():
            raise ValueError("El nombre de la encuesta es obligatorio")

        if not survey.description or not survey.description.strip():
            raise ValueError("La descripción es obligatoria")

        if not survey.created_by or survey.created_by < 1:
            raise ValueError("El ID del usuario creador es obligatorio")

        if len(survey.name_survey.strip()) > 100:
            raise ValueError("El nombre de la encuesta no puede exceder 100 caracteres")

        if len(survey.description.strip()) > 80:
            raise ValueError("La descripción no puede exceder 80 caracteres")

        return await self.repository.save(survey)