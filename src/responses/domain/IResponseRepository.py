from abc import ABC, abstractmethod
from typing import Optional, List
from src.responses.domain.entities.Response import Response

class IResponseRepository(ABC):

    @abstractmethod
    async def save(self, response: Response) -> Response:
        pass

    @abstractmethod
    async def get_all(self) -> List[Response]:
        pass

    @abstractmethod
    async def get_by_id(self, response_id: int) -> Optional[Response]:
        pass

    @abstractmethod
    async def get_by_survey(self, survey_id: int) -> List[Response]:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int) -> List[Response]:
        pass

    @abstractmethod
    async def delete(self, response_id: int) -> None:
        pass