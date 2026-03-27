from fastapi import status
from fastapi.responses import JSONResponse
from src.question_options.application.GetQuestionOptionByIdUseCase import GetQuestionOptionByIdUseCase
from src.question_options.domain.dto.QuestionOptionResponse import SingleQuestionOptionResponse, QuestionOptionResponse


class GetQuestionOptionByIdController:
    def __init__(self, get_option_by_id: GetQuestionOptionByIdUseCase):
        self.get_option_by_id = get_option_by_id

    async def execute(self, option_id: int):
        try:
            option = await self.get_option_by_id.execute(option_id)

            option_response = QuestionOptionResponse.from_question_option(option)

            response = SingleQuestionOptionResponse(option=option_response)

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
            print(f"Error al obtener opción: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )