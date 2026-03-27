from fastapi import APIRouter, Path
from src.question_options.infrastructure.controllers.CreateQuestionOptionController import CreateQuestionOptionController
from src.question_options.infrastructure.controllers.GetAllQuestionOptionsController import GetAllQuestionOptionsController
from src.question_options.infrastructure.controllers.GetQuestionOptionByIdController import GetQuestionOptionByIdController
from src.question_options.infrastructure.controllers.GetOptionsByQuestionController import GetOptionsByQuestionController
from src.question_options.infrastructure.controllers.UpdateQuestionOptionController import UpdateQuestionOptionController
from src.question_options.infrastructure.controllers.DeleteQuestionOptionController import DeleteQuestionOptionController
from src.question_options.domain.dto.QuestionOptionRequest import CreateQuestionOptionRequest, UpdateQuestionOptionRequest


def configure_question_option_routes(
    router: APIRouter,
    create_option_controller: CreateQuestionOptionController,
    get_all_options_controller: GetAllQuestionOptionsController,
    get_option_by_id_controller: GetQuestionOptionByIdController,
    get_options_by_question_controller: GetOptionsByQuestionController,
    update_option_controller: UpdateQuestionOptionController,
    delete_option_controller: DeleteQuestionOptionController
):
    @router.post("/question-options")
    async def create_question_option(request: CreateQuestionOptionRequest):
        return await create_option_controller.execute(request)

    @router.get("/question-options")
    async def get_all_question_options():
        return await get_all_options_controller.execute()

    @router.get("/question-options/{option_id}")
    async def get_question_option_by_id(option_id: int = Path(..., gt=0)):
        return await get_option_by_id_controller.execute(option_id)

    @router.get("/questions/{question_id}/options")
    async def get_options_by_question(question_id: int = Path(..., gt=0)):
        return await get_options_by_question_controller.execute(question_id)

    @router.put("/question-options/{option_id}")
    async def update_question_option(
        option_id: int = Path(..., gt=0),
        request: UpdateQuestionOptionRequest = None
    ):
        return await update_option_controller.execute(option_id, request)

    @router.delete("/question-options/{option_id}")
    async def delete_question_option(option_id: int = Path(..., gt=0)):
        return await delete_option_controller.execute(option_id)