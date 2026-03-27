from fastapi import APIRouter, Path
from src.answers.infrastructure.controllers.CreateAnswerController import CreateAnswerController
from src.answers.infrastructure.controllers.GetAllAnswersController import GetAllAnswersController
from src.answers.infrastructure.controllers.GetAnswerByIdController import GetAnswerByIdController
from src.answers.infrastructure.controllers.GetAnswersByResponseController import GetAnswersByResponseController
from src.answers.infrastructure.controllers.GetAnswersByQuestionController import GetAnswersByQuestionController
from src.answers.infrastructure.controllers.UpdateAnswerController import UpdateAnswerController
from src.answers.infrastructure.controllers.DeleteAnswerController import DeleteAnswerController
from src.answers.domain.dto.AnswerRequest import CreateAnswerRequest, UpdateAnswerRequest


def configure_answer_routes(
    router: APIRouter,
    create_answer_controller: CreateAnswerController,
    get_all_answers_controller: GetAllAnswersController,
    get_answer_by_id_controller: GetAnswerByIdController,
    get_answers_by_response_controller: GetAnswersByResponseController,
    get_answers_by_question_controller: GetAnswersByQuestionController,
    update_answer_controller: UpdateAnswerController,
    delete_answer_controller: DeleteAnswerController
):
    @router.post("/answers")
    async def create_answer(request: CreateAnswerRequest):
        return await create_answer_controller.execute(request)

    @router.get("/answers")
    async def get_all_answers():
        return await get_all_answers_controller.execute()

    @router.get("/answers/{answer_id}")
    async def get_answer_by_id(answer_id: int = Path(..., gt=0)):
        return await get_answer_by_id_controller.execute(answer_id)

    @router.get("/responses/{response_id}/answers")
    async def get_answers_by_response(response_id: int = Path(..., gt=0)):
        return await get_answers_by_response_controller.execute(response_id)

    @router.get("/questions/{question_id}/answers")
    async def get_answers_by_question(question_id: int = Path(..., gt=0)):
        return await get_answers_by_question_controller.execute(question_id)

    @router.put("/answers/{answer_id}")
    async def update_answer(
        answer_id: int = Path(..., gt=0),
        request: UpdateAnswerRequest = None
    ):
        return await update_answer_controller.execute(answer_id, request)

    @router.delete("/answers/{answer_id}")
    async def delete_answer(answer_id: int = Path(..., gt=0)):
        return await delete_answer_controller.execute(answer_id)