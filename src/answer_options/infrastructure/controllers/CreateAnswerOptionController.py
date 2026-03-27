from fastapi import status
from fastapi.responses import JSONResponse
from src.answer_options.application.CreateAnswerOptionUseCase import CreateAnswerOptionUseCase
from src.answer_options.domain.entities.AnswerOption import AnswerOption
from src.answer_options.domain.dto.AnswerOptionRequest import CreateAnswerOptionRequest
from src.answer_options.domain.dto.AnswerOptionResponse import CreateAnswerOptionResponse, CreatedAnswerOptionData


class CreateAnswerOptionController:
    def __init__(self, create_answer_option: CreateAnswerOptionUseCase):
        self.create_answer_option = create_answer_option

    async def execute(self, request: CreateAnswerOptionRequest):
        try:
            answer_option = AnswerOption(
                answer_id=request.answer_id,
                option_id=request.option_id
            )

            saved_answer_option = await self.create_answer_option.execute(answer_option)

            response = CreateAnswerOptionResponse(
                message="Opción de respuesta creada exitosamente",
                answer_option=CreatedAnswerOptionData(
                    answerOptionId=saved_answer_option.answer_option_id,
                    answerId=saved_answer_option.answer_id,
                    optionId=saved_answer_option.option_id,
                    createdAt=saved_answer_option.created_at.isoformat()
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
            print(f"Error al crear opción de respuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )