from src.core.db_postgresql import MySQLConnection
from src.responses.infrastructure.adapters.PostgreSQLResponseRepository import PostgreSQLResponseRepository
from src.responses.application.CreateResponseUseCase import CreateResponseUseCase
from src.responses.application.GetAllResponsesUseCase import GetAllResponsesUseCase
from src.responses.application.GetResponseByIdUseCase import GetResponseByIdUseCase
from src.responses.application.GetResponsesBySurveyUseCase import GetResponsesBySurveyUseCase
from src.responses.application.GetResponsesByUserUseCase import GetResponsesByUserUseCase
from src.responses.application.DeleteResponseUseCase import DeleteResponseUseCase
from src.responses.infrastructure.controllers.CreateResponseController import CreateResponseController
from src.responses.infrastructure.controllers.GetAllResponsesController import GetAllResponsesController
from src.responses.infrastructure.controllers.GetResponseByIdController import GetResponseByIdController
from src.responses.infrastructure.controllers.GetResponsesBySurveyController import GetResponsesBySurveyController
from src.responses.infrastructure.controllers.GetResponsesByUserController import GetResponsesByUserController
from src.responses.infrastructure.controllers.DeleteResponseController import DeleteResponseController


class ResponseDependencies:
    def __init__(
        self,
        create_response_controller: CreateResponseController,
        get_all_responses_controller: GetAllResponsesController,
        get_response_by_id_controller: GetResponseByIdController,
        get_responses_by_survey_controller: GetResponsesBySurveyController,
        get_responses_by_user_controller: GetResponsesByUserController,
        delete_response_controller: DeleteResponseController
    ):
        self.create_response_controller = create_response_controller
        self.get_all_responses_controller = get_all_responses_controller
        self.get_response_by_id_controller = get_response_by_id_controller
        self.get_responses_by_survey_controller = get_responses_by_survey_controller
        self.get_responses_by_user_controller = get_responses_by_user_controller
        self.delete_response_controller = delete_response_controller


def init_responses(conn: MySQLConnection) -> ResponseDependencies:
    response_repository = PostgreSQLResponseRepository(conn)

    create_response_use_case = CreateResponseUseCase(response_repository)
    get_all_responses_use_case = GetAllResponsesUseCase(response_repository)
    get_response_by_id_use_case = GetResponseByIdUseCase(response_repository)
    get_responses_by_survey_use_case = GetResponsesBySurveyUseCase(response_repository)
    get_responses_by_user_use_case = GetResponsesByUserUseCase(response_repository)
    delete_response_use_case = DeleteResponseUseCase(response_repository)

    return ResponseDependencies(
        create_response_controller=CreateResponseController(create_response_use_case),
        get_all_responses_controller=GetAllResponsesController(get_all_responses_use_case),
        get_response_by_id_controller=GetResponseByIdController(get_response_by_id_use_case),
        get_responses_by_survey_controller=GetResponsesBySurveyController(get_responses_by_survey_use_case),
        get_responses_by_user_controller=GetResponsesByUserController(get_responses_by_user_use_case),
        delete_response_controller=DeleteResponseController(delete_response_use_case)
    )