from fastapi import status
from fastapi.responses import JSONResponse
from src.answer_options.application.GetAnswerOptionsByAnswerUseCase import GetAnswerOptionsByAnswerUseCase
from src.answer_options.domain.dto.AnswerOptionResponse import AnswerOptionListResponse, AnswerOptionResponse


class GetAnswerOptionsByAnswerController:
    def __init__(self, get_answer_options_by_answer: GetAnswerOptionsByAnswerUseCase):
        self.get_answer_options_by_answer = get_answer_options_by_answer

    async def execute(self, answer_id: int):
        try:
            answer_options = await self.get_answer_options_by_answer.execute(answer_id)

            answer_option_responses = [AnswerOptionResponse.from_answer_option(ao) for ao in answer_options]

            response = AnswerOptionListResponse(
                answer_options=answer_option_responses,
                total=len(answer_option_responses)
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
            print(f"Error al obtener opciones de la respuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )