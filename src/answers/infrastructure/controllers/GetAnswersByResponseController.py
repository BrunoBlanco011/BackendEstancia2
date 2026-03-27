from fastapi import status
from fastapi.responses import JSONResponse
from src.answers.application.GetAnswersByResponseUseCase import GetAnswersByResponseUseCase
from src.answers.domain.dto.AnswerResponse import AnswerListResponse, AnswerResponse


class GetAnswersByResponseController:
    def __init__(self, get_answers_by_response: GetAnswersByResponseUseCase):
        self.get_answers_by_response = get_answers_by_response

    async def execute(self, response_id: int):
        try:
            answers = await self.get_answers_by_response.execute(response_id)

            answer_responses = [AnswerResponse.from_answer(answer) for answer in answers]

            response = AnswerListResponse(
                answers=answer_responses,
                total=len(answer_responses)
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
            print(f"Error al obtener respuestas: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )