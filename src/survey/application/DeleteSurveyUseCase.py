from src.survey.domain.ISurveyRepository import ISurveyRepository


class DeleteSurveyUseCase:
    def __init__(self, repository: ISurveyRepository):
        self.repository = repository

    async def execute(self, survey_id: int) -> None:
        if survey_id < 1:
            raise ValueError("El ID de la encuesta debe ser mayor a 0")

        existing_survey = await self.repository.get_by_id(survey_id)
        if not existing_survey:
            raise ValueError("Encuesta no encontrada")

        await self.repository.delete(survey_id)