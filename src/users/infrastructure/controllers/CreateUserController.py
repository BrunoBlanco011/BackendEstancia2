from fastapi import status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from src.users.application.CreateUserUseCase import CreateUserUseCase
from src.users.application.AuthUseCase import AuthUseCase
from src.users.domain.IUserRepository import IUserRepository
from src.users.domain.entities.User import User
from src.users.domain.dto.UserResponse import CreateUserResponse, CreatedUserData
from src.core.cloudinary_service import get_cloudinary_service
from datetime import datetime
from typing import Optional
import os
import tempfile

class CreateUserController:
    def __init__(
            self,
            create_user: CreateUserUseCase,
            auth_service: AuthUseCase,
            user_repo: IUserRepository
    ):
        self.create_user = create_user
        self.auth_service = auth_service
        self.user_repo = user_repo
        self.cloudinary_service = get_cloudinary_service()

    async def execute(
            self,
            name: str = Form(...),
            lastName: str = Form(...),
            email: str = Form(...),
            password: str = Form(...),
            roleId: int = Form(...),
            profileImage: Optional[UploadFile] = File(None)
    ):
        try:
            if not name or not lastName or not email or not password:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"error": "Faltan campos requeridos"}
                )

            profile_image_public_id = None
            if profileImage and profileImage.filename:
                allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
                if profileImage.content_type not in allowed_types:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"error": "Tipo de archivo no permitido"}
                    )

                file_content = await profileImage.read()
                if len(file_content) > 5 * 1024 * 1024:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"error": "Archivo muy grande. Máximo 5MB"}
                    )

                temp_file_path = None
                try:
                    file_extension = os.path.splitext(profileImage.filename)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                        temp_file.write(file_content)
                        temp_file_path = temp_file.name

                    result = self.cloudinary_service.upload_file(
                        temp_file_path,
                        folder="user_profiles",
                        resource_type="image"
                    )
                    profile_image_public_id = result["public_id"]
                    print(f"Public ID guardado: {profile_image_public_id}")
                finally:
                    if temp_file_path and os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

            user = User(
                name=name,
                last_name=lastName,
                email=email,
                password=password,
                role_id=roleId,
                user_id=None,
                registration_date=datetime.utcnow(),
                profile_image=profile_image_public_id
            )

            saved_user = await self.auth_service.register(user)

            print(f"Usuario {saved_user.email} registrado (roleId={saved_user.role_id})")

            profile_image_url = None
            if saved_user.profile_image:
                profile_image_url = self.cloudinary_service.get_view_url(saved_user.profile_image, "image")

            response = CreateUserResponse(
                message="Usuario creado exitosamente",
                user=CreatedUserData(
                    userId=saved_user.user_id,
                    name=saved_user.name,
                    lastName=saved_user.last_name,
                    email=saved_user.email,
                    registrationDate=saved_user.registration_date.isoformat(),
                    roleId=saved_user.role_id,
                    profileImageUrl=profile_image_url
                )
            )

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=response.model_dump()
            )

        except ValueError as error:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": str(error)}
            )
        except Exception as error:
            print(f"Error al crear usuario: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )