from fastapi import status
from fastapi.responses import JSONResponse
from src.answer_options.application.GetAllAnswerOptionsUseCase import GetAllAnswerOptionsUseCase
from src.answer_options.domain.dto.AnswerOptionResponse import AnswerOptionListResponse, AnswerOptionResponse


class GetAllAnswerOptionsController:
    def __init__(self, get_all_answer_options: GetAllAnswerOptionsUseCase):
        self.get_all_answer_options = get_all_answer_options

    async def execute(self):
        try:
            answer_options = await self.get_all_answer_options.execute()

            answer_option_responses = [AnswerOptionResponse.from_answer_option(ao) for ao in answer_options]

            response = AnswerOptionListResponse(
                answer_options=answer_option_responses,
                total=len(answer_option_responses)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except Exception as error:
            print(f"Error al obtener opciones de respuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )