from fastapi import status
from fastapi.responses import JSONResponse
from src.question_options.application.CreateQuestionOptionUseCase import CreateQuestionOptionUseCase
from src.question_options.domain.entities.QuestionOption import QuestionOption
from src.question_options.domain.dto.QuestionOptionRequest import CreateQuestionOptionRequest
from src.question_options.domain.dto.QuestionOptionResponse import CreateQuestionOptionResponse, CreatedQuestionOptionData


class CreateQuestionOptionController:
    def __init__(self, create_option: CreateQuestionOptionUseCase):
        self.create_option = create_option

    async def execute(self, request: CreateQuestionOptionRequest):
        try:
            option = QuestionOption(
                question_id=request.question_id,
                option_text=request.option_text,
                order_position=request.order_position
            )

            saved_option = await self.create_option.execute(option)

            response = CreateQuestionOptionResponse(
                message="Opción de pregunta creada exitosamente",
                option=CreatedQuestionOptionData(
                    optionId=saved_option.option_id,
                    questionId=saved_option.question_id,
                    optionText=saved_option.option_text,
                    orderPosition=saved_option.order_position,
                    createdAt=saved_option.created_at.isoformat()
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
            print(f"Error al crear opción: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )