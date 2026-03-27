from fastapi import status
from fastapi.responses import JSONResponse
from src.answers.application.GetAnswersByQuestionUseCase import GetAnswersByQuestionUseCase
from src.answers.domain.dto.AnswerResponse import AnswerListResponse, AnswerResponse


class GetAnswersByQuestionController:
    def __init__(self, get_answers_by_question: GetAnswersByQuestionUseCase):
        self.get_answers_by_question = get_answers_by_question

    async def execute(self, question_id: int):
        try:
            answers = await self.get_answers_by_question.execute(question_id)

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
            print(f"Error al obtener respuestas de la pregunta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )