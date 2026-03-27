from abc import ABC, abstractmethod
from typing import Optional, List
from src.files.domain.entities.File import File

class IFileRepository(ABC):

    @abstractmethod
    async def save(self, file: File) -> File:
        pass

    @abstractmethod
    async def get_all(self) -> List[File]:
        pass

    @abstractmethod
    async def get_by_id(self, file_id: int) -> Optional[File]:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int) -> List[File]:
        pass

    @abstractmethod
    async def delete(self, file_id: int) -> None:
        pass