from fastapi import status
from fastapi.responses import JSONResponse
from src.responses.application.GetResponseByIdUseCase import GetResponseByIdUseCase
from src.responses.domain.dto.ResponseResponse import SingleResponseResponse, ResponseResponse


class GetResponseByIdController:
    def __init__(self, get_response_by_id: GetResponseByIdUseCase):
        self.get_response_by_id = get_response_by_id

    async def execute(self, response_id: int):
        try:
            response = await self.get_response_by_id.execute(response_id)

            response_response = ResponseResponse.from_response(response)

            response_obj = SingleResponseResponse(response=response_response)

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response_obj.model_dump()
            )

        except ValueError as error:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": str(error)}
            )
        except Exception as error:
            print(f"Error al obtener respuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )