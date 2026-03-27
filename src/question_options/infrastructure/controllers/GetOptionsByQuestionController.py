from fastapi import status
from fastapi.responses import JSONResponse
from src.question_options.application.GetOptionsByQuestionUseCase import GetOptionsByQuestionUseCase
from src.question_options.domain.dto.QuestionOptionResponse import QuestionOptionListResponse, QuestionOptionResponse


class GetOptionsByQuestionController:
    def __init__(self, get_options_by_question: GetOptionsByQuestionUseCase):
        self.get_options_by_question = get_options_by_question

    async def execute(self, question_id: int):
        try:
            options = await self.get_options_by_question.execute(question_id)

            option_responses = [QuestionOptionResponse.from_question_option(option) for option in options]

            response = QuestionOptionListResponse(
                options=option_responses,
                total=len(option_responses)
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
            print(f"Error al obtener opciones de la pregunta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )