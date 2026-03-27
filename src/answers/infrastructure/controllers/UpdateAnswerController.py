from fastapi import status
from fastapi.responses import JSONResponse
from src.answers.application.UpdateAnswerUseCase import UpdateAnswerUseCase
from src.answers.application.GetAnswerByIdUseCase import GetAnswerByIdUseCase
from src.answers.domain.entities.Answer import Answer
from src.answers.domain.dto.AnswerRequest import UpdateAnswerRequest
from src.answers.domain.dto.AnswerResponse import MessageResponse


class UpdateAnswerController:
    def __init__(
        self,
        update_answer: UpdateAnswerUseCase,
        get_answer_by_id: GetAnswerByIdUseCase
    ):
        self.update_answer = update_answer
        self.get_answer_by_id = get_answer_by_id

    async def execute(self, answer_id: int, request: UpdateAnswerRequest):
        try:
            existing_answer = await self.get_answer_by_id.execute(answer_id)

            if request.answer_text is not None:
                existing_answer.answer_text = request.answer_text
            if request.selected_option_id is not None:
                existing_answer.selected_option_id = request.selected_option_id
            if request.scale_value is not None:
                existing_answer.scale_value = request.scale_value

            await self.update_answer.execute(existing_answer)

            response = MessageResponse(message="Respuesta actualizada exitosamente")

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
            print(f"Error al actualizar respuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )