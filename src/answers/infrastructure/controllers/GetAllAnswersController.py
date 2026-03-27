from fastapi import status
from fastapi.responses import JSONResponse
from src.answers.application.GetAllAnswersUseCase import GetAllAnswersUseCase
from src.answers.domain.dto.AnswerResponse import AnswerListResponse, AnswerResponse

class GetAllAnswersController:
    def __init__(self, get_all_answers: GetAllAnswersUseCase):
        self.get_all_answers = get_all_answers

    async def execute(self):
        try:
            answers = await self.get_all_answers.execute()

            answer_responses = [AnswerResponse.from_answer(answer) for answer in answers]

            response = AnswerListResponse(
                answers=answer_responses,
                total=len(answer_responses)
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