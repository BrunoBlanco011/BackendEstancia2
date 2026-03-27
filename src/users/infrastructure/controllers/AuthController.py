from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.users.application.AuthUseCase import AuthUseCase
from src.users.domain.dto.UserRequest import LoginRequest
from src.users.domain.dto.UserResponse import LoginSuccessResponse, LoginResponse, ErrorResponse
import os


class AuthController:
    def __init__(self, auth_service: AuthUseCase):
        self.auth_service = auth_service

    async def execute(self, request: LoginRequest):
        try:
            if not request.email or not request.password:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"error": "Email y password son requeridos"}
                )

            login_data = await self.auth_service.login(request.email, request.password)

            profile_image_url = None
            if login_data.get("profile_image"):
                cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
                profile_image_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/{login_data['profile_image']}"

            response = LoginSuccessResponse(
                message="Login exitoso",
                data=LoginResponse(
                    token=login_data["token"],
                    userId=login_data["userId"],
                    roleId=login_data["roleId"],
                    name=login_data["name"],
                    email=login_data["email"],
                    profileImageUrl=profile_image_url
                )
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except ValueError as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": str(error)}
            )
        except Exception as error:
            # Errores inesperados
            print(f"Error inesperado en login: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )