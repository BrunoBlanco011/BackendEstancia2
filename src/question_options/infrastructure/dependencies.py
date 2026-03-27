from src.core.db_postgresql import MySQLConnection
from src.question_options.infrastructure.adapters.PostgreSQLQuestionOptionRepository import PostgreSQLQuestionOptionRepository
from src.question_options.application.CreateQuestionOptionUseCase import CreateQuestionOptionUseCase
from src.question_options.application.GetAllQuestionOptionsUseCase import GetAllQuestionOptionsUseCase
from src.question_options.application.GetQuestionOptionByIdUseCase import GetQuestionOptionByIdUseCase
from src.question_options.application.GetOptionsByQuestionUseCase import GetOptionsByQuestionUseCase
from src.question_options.application.UpdateQuestionOptionUseCase import UpdateQuestionOptionUseCase
from src.question_options.application.DeleteQuestionOptionUseCase import DeleteQuestionOptionUseCase
from src.question_options.infrastructure.controllers.CreateQuestionOptionController import CreateQuestionOptionController
from src.question_options.infrastructure.controllers.GetAllQuestionOptionsController import GetAllQuestionOptionsController
from src.question_options.infrastructure.controllers.GetQuestionOptionByIdController import GetQuestionOptionByIdController
from src.question_options.infrastructure.controllers.GetOptionsByQuestionController import GetOptionsByQuestionController
from src.question_options.infrastructure.controllers.UpdateQuestionOptionController import UpdateQuestionOptionController
from src.question_options.infrastructure.controllers.DeleteQuestionOptionController import DeleteQuestionOptionController


class QuestionOptionDependencies:
    def __init__(
        self,
        create_option_controller: CreateQuestionOptionController,
        get_all_options_controller: GetAllQuestionOptionsController,
        get_option_by_id_controller: GetQuestionOptionByIdController,
        get_options_by_question_controller: GetOptionsByQuestionController,
        update_option_controller: UpdateQuestionOptionController,
        delete_option_controller: DeleteQuestionOptionController
    ):
        self.create_option_controller = create_option_controller
        self.get_all_options_controller = get_all_options_controller
        self.get_option_by_id_controller = get_option_by_id_controller
        self.get_options_by_question_controller = get_options_by_question_controller
        self.update_option_controller = update_option_controller
        self.delete_option_controller = delete_option_controller


def init_question_options(conn: MySQLConnection) -> QuestionOptionDependencies:
    option_repository = PostgreSQLQuestionOptionRepository(conn)

    create_option_use_case = CreateQuestionOptionUseCase(option_repository)
    get_all_options_use_case = GetAllQuestionOptionsUseCase(option_repository)
    get_option_by_id_use_case = GetQuestionOptionByIdUseCase(option_repository)
    get_options_by_question_use_case = GetOptionsByQuestionUseCase(option_repository)
    update_option_use_case = UpdateQuestionOptionUseCase(option_repository)
    delete_option_use_case = DeleteQuestionOptionUseCase(option_repository)

    return QuestionOptionDependencies(
        create_option_controller=CreateQuestionOptionController(create_option_use_case),
        get_all_options_controller=GetAllQuestionOptionsController(get_all_options_use_case),
        get_option_by_id_controller=GetQuestionOptionByIdController(get_option_by_id_use_case),
        get_options_by_question_controller=GetOptionsByQuestionController(get_options_by_question_use_case),
        update_option_controller=UpdateQuestionOptionController(
            update_option_use_case,
            get_option_by_id_use_case
        ),
        delete_option_controller=DeleteQuestionOptionController(delete_option_use_case)
    )