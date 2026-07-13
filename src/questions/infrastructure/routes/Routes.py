from fastapi import APIRouter, Path, Depends
from src.questions.infrastructure.controllers.CreateQuestionController import CreateQuestionController
from src.questions.infrastructure.controllers.GetAllQuestionsController import GetAllQuestionsController
from src.questions.infrastructure.controllers.GetQuestionByIdController import GetQuestionByIdController
from src.questions.infrastructure.controllers.GetQuestionsBySurveyController import GetQuestionsBySurveyController
from src.questions.infrastructure.controllers.UpdateQuestionController import UpdateQuestionController
from src.questions.infrastructure.controllers.DeleteQuestionController import DeleteQuestionController
from src.questions.domain.dto.QuestionRequest import CreateQuestionRequest, UpdateQuestionRequest
from src.core.security.jwt_middleware import get_current_user, UserPrincipal


def configure_question_routes(
    router: APIRouter,
    create_question_controller: CreateQuestionController,
    get_all_questions_controller: GetAllQuestionsController,
    get_question_by_id_controller: GetQuestionByIdController,
    get_questions_by_survey_controller: GetQuestionsBySurveyController,
    update_question_controller: UpdateQuestionController,
    delete_question_controller: DeleteQuestionController
):
    @router.post("/questions")
    async def create_question(
        request: CreateQuestionRequest,
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        return await create_question_controller.execute(request)

    @router.get("/questions")
    async def get_all_questions():
        return await get_all_questions_controller.execute()

    @router.get("/questions/{question_id}")
    async def get_question_by_id(question_id: int = Path(..., gt=0)):
        return await get_question_by_id_controller.execute(question_id)

    @router.get("/surveys/{survey_id}/questions")
    async def get_questions_by_survey(survey_id: int = Path(..., gt=0)):
        return await get_questions_by_survey_controller.execute(survey_id)

    @router.put("/questions/{question_id}")
    async def update_question(
        question_id: int = Path(..., gt=0),
        request: UpdateQuestionRequest = None,
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        return await update_question_controller.execute(question_id, request)

    @router.delete("/questions/{question_id}")
    async def delete_question(
        question_id: int = Path(..., gt=0),
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        return await delete_question_controller.execute(question_id)