from typing import List
from src.survey.domain.ISurveyRepository import ISurveyRepository
from src.survey.domain.entities.Survey import Survey


class GetSurveysByUserUseCase:
    def __init__(self, repository: ISurveyRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> List[Survey]:
        if user_id < 1:
            raise ValueError("El ID del usuario debe ser mayor a 0")

        return await self.repository.get_by_user(user_id)