from fastapi import status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from src.users.application.UpdateUserUseCase import UpdateUserUseCase
from src.users.domain.dto.UserResponse import MessageResponse
from src.users.domain.entities.User import User
from src.core.cloudinary_service import get_cloudinary_service
from typing import Optional
import os
import tempfile


class UpdateUserController:
    def __init__(self, update_user: UpdateUserUseCase):
        self.update_user = update_user
        self.cloudinary_service = get_cloudinary_service()

    async def execute(
            self,
            user_id: int,
            name: Optional[str] = Form(None),
            lastName: Optional[str] = Form(None),
            email: Optional[str] = Form(None),
            profileImage: Optional[UploadFile] = File(None)
    ):
        try:
            existing_user = await self.update_user.repository.get_by_id(user_id)
            if not existing_user:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"error": "Usuario no encontrado"}
                )

            new_profile_image = existing_user.profile_image
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

                if existing_user.profile_image:
                    try:
                        deleted = self.cloudinary_service.delete_file(
                            existing_user.profile_image,
                            resource_type="image"
                        )
                        if deleted:
                            print(f"Imagen anterior eliminada: {existing_user.profile_image}")
                    except Exception as e:
                        print(f"Error eliminando imagen anterior: {e}")

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
                    new_profile_image = result["public_id"]
                    print(f"Nueva imagen subida: {new_profile_image}")
                finally:
                    if temp_file_path and os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

            user = User(
                user_id=user_id,
                name=name or existing_user.name,
                last_name=lastName or existing_user.last_name,
                email=email or existing_user.email,
                password=existing_user.password,
                role_id=existing_user.role_id,
                registration_date=existing_user.registration_date,
                profile_image=new_profile_image
            )

            await self.update_user.execute(user_id, user)

            response = MessageResponse(message="Usuario actualizado exitosamente")

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except ValueError as error:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": str(error)}
            )
        except Exception as error:
            print(f"Error al actualizar usuario: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )