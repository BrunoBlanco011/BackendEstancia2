from abc import ABC, abstractmethod
from typing import Optional, List
from src.survey.domain.entities.Survey import Survey

class ISurveyRepository(ABC):

    @abstractmethod
    async def save(self, survey: Survey) -> Survey:
        pass

    @abstractmethod
    async def get_all(self) -> List[Survey]:
        pass

    @abstractmethod
    async def get_by_id(self, survey_id: int) -> Optional[Survey]:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int) -> List[Survey]:
        pass

    @abstractmethod
    async def update(self, survey: Survey) -> None:
        pass

    @abstractmethod
    async def delete(self, survey_id: int) -> None:
        pass