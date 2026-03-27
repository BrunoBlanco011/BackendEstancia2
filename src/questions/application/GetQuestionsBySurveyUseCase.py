from typing import List
from src.questions.domain.IQuestionRepository import IQuestionRepository
from src.questions.domain.entities.Question import Question


class GetQuestionsBySurveyUseCase:
    def __init__(self, repository: IQuestionRepository):
        self.repository = repository

    async def execute(self, survey_id: int) -> List[Question]:
        if survey_id < 1:
            raise ValueError("El ID de la encuesta debe ser mayor a 0")

        return await self.repository.get_by_survey(survey_id)