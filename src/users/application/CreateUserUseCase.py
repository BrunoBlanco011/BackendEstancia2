from src.users.domain.IUserRepository import IUserRepository
from src.users.domain.entities.User import User


class CreateUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, user: User) -> User:
        if not user.name or not user.name.strip():
            raise ValueError("El nombre es obligatorio")

        if not user.last_name or not user.last_name.strip():
            raise ValueError("El apellido es obligatorio")

        if not user.email or not user.email.strip():
            raise ValueError("El email es obligatorio")

        existing_user = await self.repository.get_by_email(user.email.strip())
        if existing_user is not None:
            raise ValueError("El email ya está registrado")

        if not user.password or len(user.password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")

        if not user.role_id or user.role_id < 1:
            raise ValueError("El rol es obligatorio")

        return await self.repository.save(user)