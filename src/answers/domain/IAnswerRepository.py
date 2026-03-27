from abc import ABC, abstractmethod
from typing import Optional, List
from src.answers.domain.entities.Answer import Answer

class IAnswerRepository(ABC):

    @abstractmethod
    async def save(self, answer: Answer) -> Answer:
        pass

    @abstractmethod
    async def get_all(self) -> List[Answer]:
        pass

    @abstractmethod
    async def get_by_id(self, answer_id: int) -> Optional[Answer]:
        pass

    @abstractmethod
    async def get_by_response(self, response_id: int) -> List[Answer]:
        pass

    @abstractmethod
    async def get_by_question(self, question_id: int) -> List[Answer]:
        pass

    @abstractmethod
    async def update(self, answer: Answer) -> None:
        pass

    @abstractmethod
    async def delete(self, answer_id: int) -> None:
        pass