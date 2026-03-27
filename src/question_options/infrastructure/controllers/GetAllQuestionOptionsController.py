from fastapi import status
from fastapi.responses import JSONResponse
from src.question_options.application.GetAllQuestionOptionsUseCase import GetAllQuestionOptionsUseCase
from src.question_options.domain.dto.QuestionOptionResponse import QuestionOptionListResponse, QuestionOptionResponse


class GetAllQuestionOptionsController:
    def __init__(self, get_all_options: GetAllQuestionOptionsUseCase):
        self.get_all_options = get_all_options

    async def execute(self):
        try:
            options = await self.get_all_options.execute()

            option_responses = [QuestionOptionResponse.from_question_option(option) for option in options]

            response = QuestionOptionListResponse(
                options=option_responses,
                total=len(option_responses)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=response.model_dump()
            )

        except Exception as error:
            print(f"Error al obtener opciones: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )