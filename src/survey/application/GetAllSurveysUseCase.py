from typing import List
from src.survey.domain.ISurveyRepository import ISurveyRepository
from src.survey.domain.entities.Survey import Survey


class GetAllSurveysUseCase:
    def __init__(self, repository: ISurveyRepository):
        self.repository = repository

    async def execute(self) -> List[Survey]:
        return await self.repository.get_all()