from fastapi import APIRouter, Path, Depends
from src.answer_options.infrastructure.controllers.CreateAnswerOptionController import CreateAnswerOptionController
from src.answer_options.infrastructure.controllers.GetAllAnswerOptionsController import GetAllAnswerOptionsController
from src.answer_options.infrastructure.controllers.GetAnswerOptionByIdController import GetAnswerOptionByIdController
from src.answer_options.infrastructure.controllers.GetAnswerOptionsByAnswerController import GetAnswerOptionsByAnswerController
from src.answer_options.infrastructure.controllers.DeleteAnswerOptionController import DeleteAnswerOptionController
from src.answer_options.domain.dto.AnswerOptionRequest import CreateAnswerOptionRequest
from src.core.security.jwt_middleware import get_current_user, UserPrincipal


def configure_answer_option_routes(
    router: APIRouter,
    create_answer_option_controller: CreateAnswerOptionController,
    get_all_answer_options_controller: GetAllAnswerOptionsController,
    get_answer_option_by_id_controller: GetAnswerOptionByIdController,
    get_answer_options_by_answer_controller: GetAnswerOptionsByAnswerController,
    delete_answer_option_controller: DeleteAnswerOptionController
):
    @router.post("/answer-options")
    async def create_answer_option(
        request: CreateAnswerOptionRequest,
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        return await create_answer_option_controller.execute(request)

    @router.get("/answer-options")
    async def get_all_answer_options(current_user: UserPrincipal = Depends(get_current_user)):
        return await get_all_answer_options_controller.execute()

    @router.get("/answer-options/{answer_option_id}")
    async def get_answer_option_by_id(
        answer_option_id: int = Path(..., gt=0),
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        return await get_answer_option_by_id_controller.execute(answer_option_id)

    @router.get("/answers/{answer_id}/answer-options")
    async def get_answer_options_by_answer(
        answer_id: int = Path(..., gt=0),
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        return await get_answer_options_by_answer_controller.execute(answer_id)

    @router.delete("/answer-options/{answer_option_id}")
    async def delete_answer_option(
        answer_option_id: int = Path(..., gt=0),
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        return await delete_answer_option_controller.execute(answer_option_id)