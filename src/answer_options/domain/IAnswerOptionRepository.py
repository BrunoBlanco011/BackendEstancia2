from abc import ABC, abstractmethod
from typing import Optional, List
from src.answer_options.domain.entities.AnswerOption import AnswerOption

class IAnswerOptionRepository(ABC):

    @abstractmethod
    async def save(self, answer_option: AnswerOption) -> AnswerOption:
        pass

    @abstractmethod
    async def get_all(self) -> List[AnswerOption]:
        pass

    @abstractmethod
    async def get_by_id(self, answer_option_id: int) -> Optional[AnswerOption]:
        pass

    @abstractmethod
    async def get_by_answer(self, answer_id: int) -> List[AnswerOption]:
        pass

    @abstractmethod
    async def delete(self, answer_option_id: int) -> None:
        pass