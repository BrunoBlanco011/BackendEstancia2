from fastapi import status
from fastapi.responses import JSONResponse
from src.question_options.application.UpdateQuestionOptionUseCase import UpdateQuestionOptionUseCase
from src.question_options.application.GetQuestionOptionByIdUseCase import GetQuestionOptionByIdUseCase
from src.question_options.domain.entities.QuestionOption import QuestionOption
from src.question_options.domain.dto.QuestionOptionRequest import UpdateQuestionOptionRequest
from src.question_options.domain.dto.QuestionOptionResponse import MessageResponse


class UpdateQuestionOptionController:
    def __init__(
        self,
        update_option: UpdateQuestionOptionUseCase,
        get_option_by_id: GetQuestionOptionByIdUseCase
    ):
        self.update_option = update_option
        self.get_option_by_id = get_option_by_id

    async def execute(self, option_id: int, request: UpdateQuestionOptionRequest):
        try:
            existing_option = await self.get_option_by_id.execute(option_id)

            if request.option_text is not None:
                existing_option.option_text = request.option_text
            if request.order_position is not None:
                existing_option.order_position = request.order_position

            await self.update_option.execute(existing_option)

            response = MessageResponse(message="Opción actualizada exitosamente")

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
            print(f"Error al actualizar opción: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )