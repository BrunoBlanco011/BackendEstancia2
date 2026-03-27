from abc import ABC, abstractmethod
from typing import Optional, List
from src.questions.domain.entities.Question import Question

class IQuestionRepository(ABC):

    @abstractmethod
    async def save(self, question: Question) -> Question:
        pass

    @abstractmethod
    async def get_all(self) -> List[Question]:
        pass

    @abstractmethod
    async def get_by_id(self, question_id: int) -> Optional[Question]:
        pass

    @abstractmethod
    async def get_by_survey(self, survey_id: int) -> List[Question]:
        pass

    @abstractmethod
    async def update(self, question: Question) -> None:
        pass

    @abstractmethod
    async def delete(self, question_id: int) -> None:
        pass