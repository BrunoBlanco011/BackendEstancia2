from src.core.db_postgresql import MySQLConnection
from src.answer_options.infrastructure.adapters.PostgreSQLAnswerOptionRepository import PostgreSQLAnswerOptionRepository
from src.answer_options.application.CreateAnswerOptionUseCase import CreateAnswerOptionUseCase
from src.answer_options.application.GetAllAnswerOptionsUseCase import GetAllAnswerOptionsUseCase
from src.answer_options.application.GetAnswerOptionByIdUseCase import GetAnswerOptionByIdUseCase
from src.answer_options.application.GetAnswerOptionsByAnswerUseCase import GetAnswerOptionsByAnswerUseCase
from src.answer_options.application.DeleteAnswerOptionUseCase import DeleteAnswerOptionUseCase
from src.answer_options.infrastructure.controllers.CreateAnswerOptionController import CreateAnswerOptionController
from src.answer_options.infrastructure.controllers.GetAllAnswerOptionsController import GetAllAnswerOptionsController
from src.answer_options.infrastructure.controllers.GetAnswerOptionByIdController import GetAnswerOptionByIdController
from src.answer_options.infrastructure.controllers.GetAnswerOptionsByAnswerController import GetAnswerOptionsByAnswerController
from src.answer_options.infrastructure.controllers.DeleteAnswerOptionController import DeleteAnswerOptionController


class AnswerOptionDependencies:
    def __init__(
        self,
        create_answer_option_controller: CreateAnswerOptionController,
        get_all_answer_options_controller: GetAllAnswerOptionsController,
        get_answer_option_by_id_controller: GetAnswerOptionByIdController,
        get_answer_options_by_answer_controller: GetAnswerOptionsByAnswerController,
        delete_answer_option_controller: DeleteAnswerOptionController
    ):
        self.create_answer_option_controller = create_answer_option_controller
        self.get_all_answer_options_controller = get_all_answer_options_controller
        self.get_answer_option_by_id_controller = get_answer_option_by_id_controller
        self.get_answer_options_by_answer_controller = get_answer_options_by_answer_controller
        self.delete_answer_option_controller = delete_answer_option_controller


def init_answer_options(conn: MySQLConnection) -> AnswerOptionDependencies:
    answer_option_repository = PostgreSQLAnswerOptionRepository(conn)

    create_answer_option_use_case = CreateAnswerOptionUseCase(answer_option_repository)
    get_all_answer_options_use_case = GetAllAnswerOptionsUseCase(answer_option_repository)
    get_answer_option_by_id_use_case = GetAnswerOptionByIdUseCase(answer_option_repository)
    get_answer_options_by_answer_use_case = GetAnswerOptionsByAnswerUseCase(answer_option_repository)
    delete_answer_option_use_case = DeleteAnswerOptionUseCase(answer_option_repository)

    return AnswerOptionDependencies(
        create_answer_option_controller=CreateAnswerOptionController(create_answer_option_use_case),
        get_all_answer_options_controller=GetAllAnswerOptionsController(get_all_answer_options_use_case),
        get_answer_option_by_id_controller=GetAnswerOptionByIdController(get_answer_option_by_id_use_case),
        get_answer_options_by_answer_controller=GetAnswerOptionsByAnswerController(get_answer_options_by_answer_use_case),
        delete_answer_option_controller=DeleteAnswerOptionController(delete_answer_option_use_case)
    )