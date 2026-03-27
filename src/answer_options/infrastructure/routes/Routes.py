from fastapi import APIRouter, Path
from src.answer_options.infrastructure.controllers.CreateAnswerOptionController import CreateAnswerOptionController
from src.answer_options.infrastructure.controllers.GetAllAnswerOptionsController import GetAllAnswerOptionsController
from src.answer_options.infrastructure.controllers.GetAnswerOptionByIdController import GetAnswerOptionByIdController
from src.answer_options.infrastructure.controllers.GetAnswerOptionsByAnswerController import GetAnswerOptionsByAnswerController
from src.answer_options.infrastructure.controllers.DeleteAnswerOptionController import DeleteAnswerOptionController
from src.answer_options.domain.dto.AnswerOptionRequest import CreateAnswerOptionRequest


def configure_answer_option_routes(
    router: APIRouter,
    create_answer_option_controller: CreateAnswerOptionController,
    get_all_answer_options_controller: GetAllAnswerOptionsController,
    get_answer_option_by_id_controller: GetAnswerOptionByIdController,
    get_answer_options_by_answer_controller: GetAnswerOptionsByAnswerController,
    delete_answer_option_controller: DeleteAnswerOptionController
):
    @router.post("/answer-options")
    async def create_answer_option(request: CreateAnswerOptionRequest):
        return await create_answer_option_controller.execute(request)

    @router.get("/answer-options")
    async def get_all_answer_options():
        return await get_all_answer_options_controller.execute()

    @router.get("/answer-options/{answer_option_id}")
    async def get_answer_option_by_id(answer_option_id: int = Path(..., gt=0)):
        return await get_answer_option_by_id_controller.execute(answer_option_id)

    @router.get("/answers/{answer_id}/answer-options")
    async def get_answer_options_by_answer(answer_id: int = Path(..., gt=0)):
        return await get_answer_options_by_answer_controller.execute(answer_id)

    @router.delete("/answer-options/{answer_option_id}")
    async def delete_answer_option(answer_option_id: int = Path(..., gt=0)):
        return await delete_answer_option_controller.execute(answer_option_id)