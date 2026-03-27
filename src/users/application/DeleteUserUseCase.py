from src.users.domain.IUserRepository import IUserRepository

class DeleteUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> None:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        await self.repository.delete(user_id)