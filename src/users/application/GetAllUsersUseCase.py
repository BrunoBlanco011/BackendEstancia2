from typing import List
from src.users.domain.IUserRepository import IUserRepository
from src.users.domain.entities.User import User

class GetAllUsersUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self) -> List[User]:
        return await self.repository.get_all()