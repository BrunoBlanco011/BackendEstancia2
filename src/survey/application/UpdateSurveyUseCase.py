from src.survey.domain.ISurveyRepository import ISurveyRepository
from src.survey.domain.entities.Survey import Survey


class UpdateSurveyUseCase:
    def __init__(self, repository: ISurveyRepository):
        self.repository = repository

    async def execute(self, survey: Survey) -> None:
        if not survey.survey_id or survey.survey_id < 1:
            raise ValueError("El ID de la encuesta es obligatorio")

        existing_survey = await self.repository.get_by_id(survey.survey_id)
        if not existing_survey:
            raise ValueError("Encuesta no encontrada")

        if survey.name_survey and len(survey.name_survey.strip()) > 100:
            raise ValueError("El nombre de la encuesta no puede exceder 100 caracteres")

        if survey.description and len(survey.description.strip()) > 80:
            raise ValueError("La descripción no puede exceder 80 caracteres")

        await self.repository.update(survey)