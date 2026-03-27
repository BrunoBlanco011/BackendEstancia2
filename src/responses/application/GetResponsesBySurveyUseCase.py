from typing import List
from src.responses.domain.IResponseRepository import IResponseRepository
from src.responses.domain.entities.Response import Response


class GetResponsesBySurveyUseCase:
    def __init__(self, repository: IResponseRepository):
        self.repository = repository

    async def execute(self, survey_id: int) -> List[Response]:
        if survey_id < 1:
            raise ValueError("El ID de la encuesta debe ser mayor a 0")

        return await self.repository.get_by_survey(survey_id)