from typing import Optional
from datetime import datetime
from src.users.domain.IUserRepository import IUserRepository
from src.users.domain.entities.User import User
from src.core.security.hash import HashService
from src.core.security.auth import AuthService


class AuthUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def login(self, email: str, password: str) -> dict:
        trimmed_email = email.strip()
        print(f"Buscando usuario con correo: {trimmed_email}")

        user = await self.repository.get_by_email(trimmed_email)

        if user is None:
            print("Usuario no encontrado (None)")
            raise ValueError("Usuario no encontrado")

        is_valid_password = HashService.check_password(user.password, password)

        if not is_valid_password:
            print("Contraseña incorrecta")
            raise ValueError("Contraseña incorrecta")

        print(f"Usuario {user.user_id} - RoleId: {user.role_id}")

        token = AuthService.generate_jwt(user.user_id, user.email)

        return {
            "token": token,
            "userId": user.user_id,
            "roleId": user.role_id,
            "name": user.name,
            "email": user.email,
            "profile_image": user.profile_image
        }

    async def register(self, user: User) -> User:
        existing_user = await self.repository.get_by_email(user.email)
        if existing_user is not None:
            raise ValueError("El email ya esta registrado")

        hashed_password = HashService.hash_password(user.password)

        user.password = hashed_password
        user.registration_date = datetime.utcnow()

        return await self.repository.save(user)