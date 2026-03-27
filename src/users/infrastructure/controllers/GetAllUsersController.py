from fastapi import status
from fastapi.responses import JSONResponse
from src.users.application.GetAllUsersUseCase import GetAllUsersUseCase
from src.users.domain.dto.UserResponse import UserListResponse, UserResponse, ErrorResponse

class GetAllUsersController:
    def __init__(self, get_all_users: GetAllUsersUseCase):
        self.get_all_users = get_all_users

    async def execute(self):
        try:
            users = await self.get_all_users.execute()

            user_responses = [UserResponse.from_user(user) for user in users]

            response = UserListResponse(
                users=user_responses,
                total=len(user_responses)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except Exception as error:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": str(error) if str(error) else "Error desconocido"}
            )