from fastapi import status
from fastapi.responses import JSONResponse
from src.responses.application.GetAllResponsesUseCase import GetAllResponsesUseCase
from src.responses.domain.dto.ResponseResponse import ResponseListResponse, ResponseResponse


class GetAllResponsesController:
    def __init__(self, get_all_responses: GetAllResponsesUseCase):
        self.get_all_responses = get_all_responses

    async def execute(self):
        try:
            responses = await self.get_all_responses.execute()

            response_responses = [ResponseResponse.from_response(response) for response in responses]

            response = ResponseListResponse(
                responses=response_responses,
                total=len(response_responses)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except Exception as error:
            print(f"Error al obtener respuestas: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )