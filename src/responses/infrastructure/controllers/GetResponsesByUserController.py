from fastapi import status
from fastapi.responses import JSONResponse
from src.responses.application.GetResponsesByUserUseCase import GetResponsesByUserUseCase
from src.responses.domain.dto.ResponseResponse import ResponseListResponse, ResponseResponse


class GetResponsesByUserController:
    def __init__(self, get_responses_by_user: GetResponsesByUserUseCase):
        self.get_responses_by_user = get_responses_by_user

    async def execute(self, user_id: int):
        try:
            responses = await self.get_responses_by_user.execute(user_id)

            response_responses = [ResponseResponse.from_response(response) for response in responses]

            response = ResponseListResponse(
                responses=response_responses,
                total=len(response_responses)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except ValueError as error:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": str(error)}
            )
        except Exception as error:
            print(f"Error al obtener respuestas del usuario: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )