from src.users.domain.IUserRepository import IUserRepository
from src.users.domain.entities.User import User

class UpdateUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, user_id: int, user: User) -> None:
        existing_user = await self.repository.get_by_id(user_id)
        if not existing_user:
            raise ValueError("Usuario no encontrado")

        if user.email and user.email != existing_user.email:
            email_exists = await self.repository.get_by_email(user.email)
            if email_exists:
                raise ValueError("El email ya esta en uso")

        await self.repository.update(user)