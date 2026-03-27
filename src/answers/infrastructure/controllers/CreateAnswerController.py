from fastapi import status
from fastapi.responses import JSONResponse
from src.answers.application.CreateAnswerUseCase import CreateAnswerUseCase
from src.answers.domain.entities.Answer import Answer
from src.answers.domain.dto.AnswerRequest import CreateAnswerRequest
from src.answers.domain.dto.AnswerResponse import CreateAnswerResponse, CreatedAnswerData

class CreateAnswerController:
    def __init__(self, create_answer: CreateAnswerUseCase):
        self.create_answer = create_answer

    async def execute(self, request: CreateAnswerRequest):
        try:
            answer = Answer(
                response_id=request.response_id,
                question_id=request.question_id,
                answer_text=request.answer_text,
                selected_option_id=request.selected_option_id,
                scale_value=request.scale_value
            )

            saved_answer = await self.create_answer.execute(answer)

            response = CreateAnswerResponse(
                message="Respuesta creada exitosamente",
                answer=CreatedAnswerData(
                    answerId=saved_answer.answer_id,
                    responseId=saved_answer.response_id,
                    questionId=saved_answer.question_id,
                    answerText=saved_answer.answer_text,
                    selectedOptionId=saved_answer.selected_option_id,
                    scaleValue=saved_answer.scale_value,
                    createdAt=saved_answer.created_at.isoformat()
                )
            )

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=response.model_dump()
            )

        except ValueError as error:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": str(error)}
            )
        except Exception as error:
            print(f"Error al crear respuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )