from fastapi import status
from fastapi.responses import JSONResponse
from src.answer_options.application.GetAnswerOptionByIdUseCase import GetAnswerOptionByIdUseCase
from src.answer_options.domain.dto.AnswerOptionResponse import SingleAnswerOptionResponse, AnswerOptionResponse


class GetAnswerOptionByIdController:
    def __init__(self, get_answer_option_by_id: GetAnswerOptionByIdUseCase):
        self.get_answer_option_by_id = get_answer_option_by_id

    async def execute(self, answer_option_id: int):
        try:
            answer_option = await self.get_answer_option_by_id.execute(answer_option_id)

            answer_option_response = AnswerOptionResponse.from_answer_option(answer_option)

            response = SingleAnswerOptionResponse(answer_option=answer_option_response)

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
            print(f"Error al obtener opción de respuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )