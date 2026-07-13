from fastapi import APIRouter, Path, Depends
from src.survey.infrastructure.controllers.CreateSurveyController import CreateSurveyController
from src.survey.infrastructure.controllers.GetAllSurveysController import GetAllSurveysController
from src.survey.infrastructure.controllers.GetSurveyByIdController import GetSurveyByIdController
from src.survey.infrastructure.controllers.GetSurveysByUserController import GetSurveysByUserController
from src.survey.infrastructure.controllers.UpdateSurveyController import UpdateSurveyController
from src.survey.infrastructure.controllers.DeleteSurveyController import DeleteSurveyController
from src.survey.domain.dto.SurveyRequest import CreateSurveyRequest, UpdateSurveyRequest
from src.core.security.jwt_middleware import get_current_user, UserPrincipal


def configure_survey_routes(
    router: APIRouter,
    create_survey_controller: CreateSurveyController,
    get_all_surveys_controller: GetAllSurveysController,
    get_survey_by_id_controller: GetSurveyByIdController,
    get_surveys_by_user_controller: GetSurveysByUserController,
    update_survey_controller: UpdateSurveyController,
    delete_survey_controller: DeleteSurveyController
):
    @router.post("/surveys")
    async def create_survey(
        request: CreateSurveyRequest,
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        return await create_survey_controller.execute(request)

    @router.get("/surveys")
    async def get_all_surveys():
        return await get_all_surveys_controller.execute()

    @router.get("/surveys/{survey_id}")
    async def get_survey_by_id(survey_id: int = Path(..., gt=0)):
        return await get_survey_by_id_controller.execute(survey_id)

    @router.get("/users/{user_id}/surveys")
    async def get_surveys_by_user(
        user_id: int = Path(..., gt=0),
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        return await get_surveys_by_user_controller.execute(user_id)

    @router.put("/surveys/{survey_id}")
    async def update_survey(
        survey_id: int = Path(..., gt=0),
        request: UpdateSurveyRequest = None,
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        return await update_survey_controller.execute(survey_id, request)

    @router.delete("/surveys/{survey_id}")
    async def delete_survey(
        survey_id: int = Path(..., gt=0),
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        return await delete_survey_controller.execute(survey_id)