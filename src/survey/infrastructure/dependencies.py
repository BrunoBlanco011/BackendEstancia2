from src.core.db_postgresql import MySQLConnection
from src.survey.infrastructure.adapters.PostgreSQLSurveyRepository import PostgreSQLSurveyRepository
from src.survey.application.CreateSurveyUseCase import CreateSurveyUseCase
from src.survey.application.GetAllSurveysUseCase import GetAllSurveysUseCase
from src.survey.application.GetSurveyByIdUseCase import GetSurveyByIdUseCase
from src.survey.application.GetSurveysByUserUseCase import GetSurveysByUserUseCase
from src.survey.application.UpdateSurveyUseCase import UpdateSurveyUseCase
from src.survey.application.DeleteSurveyUseCase import DeleteSurveyUseCase
from src.survey.infrastructure.controllers.CreateSurveyController import CreateSurveyController
from src.survey.infrastructure.controllers.GetAllSurveysController import GetAllSurveysController
from src.survey.infrastructure.controllers.GetSurveyByIdController import GetSurveyByIdController
from src.survey.infrastructure.controllers.GetSurveysByUserController import GetSurveysByUserController
from src.survey.infrastructure.controllers.UpdateSurveyController import UpdateSurveyController
from src.survey.infrastructure.controllers.DeleteSurveyController import DeleteSurveyController


class SurveyDependencies:
    def __init__(
        self,
        create_survey_controller: CreateSurveyController,
        get_all_surveys_controller: GetAllSurveysController,
        get_survey_by_id_controller: GetSurveyByIdController,
        get_surveys_by_user_controller: GetSurveysByUserController,
        update_survey_controller: UpdateSurveyController,
        delete_survey_controller: DeleteSurveyController
    ):
        self.create_survey_controller = create_survey_controller
        self.get_all_surveys_controller = get_all_surveys_controller
        self.get_survey_by_id_controller = get_survey_by_id_controller
        self.get_surveys_by_user_controller = get_surveys_by_user_controller
        self.update_survey_controller = update_survey_controller
        self.delete_survey_controller = delete_survey_controller


def init_surveys(conn: MySQLConnection) -> SurveyDependencies:
    survey_repository = PostgreSQLSurveyRepository(conn)

    create_survey_use_case = CreateSurveyUseCase(survey_repository)
    get_all_surveys_use_case = GetAllSurveysUseCase(survey_repository)
    get_survey_by_id_use_case = GetSurveyByIdUseCase(survey_repository)
    get_surveys_by_user_use_case = GetSurveysByUserUseCase(survey_repository)
    update_survey_use_case = UpdateSurveyUseCase(survey_repository)
    delete_survey_use_case = DeleteSurveyUseCase(survey_repository)

    return SurveyDependencies(
        create_survey_controller=CreateSurveyController(create_survey_use_case),
        get_all_surveys_controller=GetAllSurveysController(get_all_surveys_use_case),
        get_survey_by_id_controller=GetSurveyByIdController(get_survey_by_id_use_case),
        get_surveys_by_user_controller=GetSurveysByUserController(get_surveys_by_user_use_case),
        update_survey_controller=UpdateSurveyController(
            update_survey_use_case,
            get_survey_by_id_use_case
        ),
        delete_survey_controller=DeleteSurveyController(delete_survey_use_case)
    )