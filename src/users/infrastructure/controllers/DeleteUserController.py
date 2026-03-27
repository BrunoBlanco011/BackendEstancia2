from fastapi import status
from fastapi.responses import JSONResponse
from src.users.application.DeleteUserUseCase import DeleteUserUseCase
from src.users.domain.dto.UserResponse import MessageResponse, ErrorResponse
from src.core.cloudinary_service import get_cloudinary_service


class DeleteUserController:
    def __init__(self, delete_user: DeleteUserUseCase):
        self.delete_user = delete_user
        self.cloudinary_service = get_cloudinary_service()

    async def execute(self, user_id: int):
        try:
            user = await self.delete_user.repository.get_by_id(user_id)
            if not user:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"error": "Usuario no encontrado"}
                )

            if user.profile_image:
                try:
                    deleted = self.cloudinary_service.delete_file(
                        user.profile_image,
                        resource_type="image"
                    )
                    if deleted:
                        print(f"Imagen eliminada: {user.profile_image}")
                    else:
                        print(f"No se pudo eliminar la imagen: {user.profile_image}")
                except Exception as e:
                    print(f"Error eliminando imagen de Cloudinary: {e}")

            await self.delete_user.execute(user_id)

            response = MessageResponse(message="Usuario eliminado exitosamente")

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
            print(f"Error al eliminar usuario: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )