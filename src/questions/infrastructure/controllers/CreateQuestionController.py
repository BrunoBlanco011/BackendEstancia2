from fastapi import status
from fastapi.responses import JSONResponse
from src.questions.application.CreateQuestionUseCase import CreateQuestionUseCase
from src.questions.domain.entities.Question import Question
from src.questions.domain.dto.QuestionRequest import CreateQuestionRequest
from src.questions.domain.dto.QuestionResponse import CreateQuestionResponse, CreatedQuestionData

class CreateQuestionController:
    def __init__(self, create_question: CreateQuestionUseCase):
        self.create_question = create_question

    async def execute(self, request: CreateQuestionRequest):
        try:
            question = Question(
                survey_id=request.survey_id,
                question_text=request.question_text,
                question_type=request.question_type,
                is_required=request.is_required,
                order_position=request.order_position
            )

            saved_question = await self.create_question.execute(question)

            response = CreateQuestionResponse(
                message="Pregunta creada exitosamente",
                question=CreatedQuestionData(
                    questionId=saved_question.question_id,
                    surveyId=saved_question.survey_id,
                    questionText=saved_question.question_text,
                    questionType=saved_question.question_type,
                    isRequired=saved_question.is_required,
                    orderPosition=saved_question.order_position,
                    createdAt=saved_question.created_at.isoformat()
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
            print(f"Error al crear pregunta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )