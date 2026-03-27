from abc import ABC, abstractmethod
from typing import Optional, List
from src.question_options.domain.entities.QuestionOption import QuestionOption

class IQuestionOptionRepository(ABC):

    @abstractmethod
    async def save(self, option: QuestionOption) -> QuestionOption:
        pass

    @abstractmethod
    async def get_all(self) -> List[QuestionOption]:
        pass

    @abstractmethod
    async def get_by_id(self, option_id: int) -> Optional[QuestionOption]:
        pass

    @abstractmethod
    async def get_by_question(self, question_id: int) -> List[QuestionOption]:
        pass

    @abstractmethod
    async def update(self, option: QuestionOption) -> None:
        pass

    @abstractmethod
    async def delete(self, option_id: int) -> None:
        pass