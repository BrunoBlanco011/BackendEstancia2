from typing import Optional
from src.users.domain.IUserRepository import IUserRepository
from src.users.domain.entities.User import User

class GetUserByIdUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> Optional[User]:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        return user