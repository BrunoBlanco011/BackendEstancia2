from fastapi import status
from fastapi.responses import JSONResponse
from src.users.application.GetUserByIdUseCase import GetUserByIdUseCase
from src.users.domain.dto.UserResponse import SingleUserResponse, UserResponse, ErrorResponse

class GetUserByIdController:
    def __init__(self, get_user_by_id: GetUserByIdUseCase):
        self.get_user_by_id = get_user_by_id

    async def execute(self, user_id: int):
        try:
            user = await self.get_user_by_id.execute(user_id)

            response = SingleUserResponse(
                user=UserResponse.from_user(user)
            )

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
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": str(error) if str(error) else "Error desconocido"}
            )