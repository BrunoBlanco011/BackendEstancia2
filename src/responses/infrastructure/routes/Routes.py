from fastapi import APIRouter, Path, Request
from src.responses.infrastructure.controllers.CreateResponseController import CreateResponseController
from src.responses.infrastructure.controllers.GetAllResponsesController import GetAllResponsesController
from src.responses.infrastructure.controllers.GetResponseByIdController import GetResponseByIdController
from src.responses.infrastructure.controllers.GetResponsesBySurveyController import GetResponsesBySurveyController
from src.responses.infrastructure.controllers.GetResponsesByUserController import GetResponsesByUserController
from src.responses.infrastructure.controllers.DeleteResponseController import DeleteResponseController
from src.responses.domain.dto.ResponseRequest import CreateResponseRequest


def configure_response_routes(
    router: APIRouter,
    create_response_controller: CreateResponseController,
    get_all_responses_controller: GetAllResponsesController,
    get_response_by_id_controller: GetResponseByIdController,
    get_responses_by_survey_controller: GetResponsesBySurveyController,
    get_responses_by_user_controller: GetResponsesByUserController,
    delete_response_controller: DeleteResponseController
):
    @router.post("/responses")
    async def create_response(request_data: CreateResponseRequest, request: Request):
        return await create_response_controller.execute(request_data, request)

    @router.get("/responses")
    async def get_all_responses():
        return await get_all_responses_controller.execute()

    @router.get("/responses/{response_id}")
    async def get_response_by_id(response_id: int = Path(..., gt=0)):
        return await get_response_by_id_controller.execute(response_id)

    @router.get("/surveys/{survey_id}/responses")
    async def get_responses_by_survey(survey_id: int = Path(..., gt=0)):
        return await get_responses_by_survey_controller.execute(survey_id)

    @router.get("/users/{user_id}/responses")
    async def get_responses_by_user(user_id: int = Path(..., gt=0)):
        return await get_responses_by_user_controller.execute(user_id)

    @router.delete("/responses/{response_id}")
    async def delete_response(response_id: int = Path(..., gt=0)):
        return await delete_response_controller.execute(response_id)