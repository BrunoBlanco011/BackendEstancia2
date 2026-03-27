from fastapi import status
from fastapi.responses import JSONResponse
from src.answers.application.GetAnswerByIdUseCase import GetAnswerByIdUseCase
from src.answers.domain.dto.AnswerResponse import SingleAnswerResponse, AnswerResponse


class GetAnswerByIdController:
    def __init__(self, get_answer_by_id: GetAnswerByIdUseCase):
        self.get_answer_by_id = get_answer_by_id

    async def execute(self, answer_id: int):
        try:
            answer = await self.get_answer_by_id.execute(answer_id)

            answer_response = AnswerResponse.from_answer(answer)

            response = SingleAnswerResponse(answer=answer_response)

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
            print(f"Error al obtener respuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )