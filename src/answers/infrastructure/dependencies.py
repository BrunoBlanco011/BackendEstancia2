from src.core.db_postgresql import MySQLConnection
from src.answers.infrastructure.adapters.PostgreSQLAnswerRepository import PostgreSQLAnswerRepository
from src.answers.application.CreateAnswerUseCase import CreateAnswerUseCase
from src.answers.application.GetAllAnswersUseCase import GetAllAnswersUseCase
from src.answers.application.GetAnswerByIdUseCase import GetAnswerByIdUseCase
from src.answers.application.GetAnswersByResponseUseCase import GetAnswersByResponseUseCase
from src.answers.application.GetAnswersByQuestionUseCase import GetAnswersByQuestionUseCase
from src.answers.application.UpdateAnswerUseCase import UpdateAnswerUseCase
from src.answers.application.DeleteAnswerUseCase import DeleteAnswerUseCase
from src.answers.infrastructure.controllers.CreateAnswerController import CreateAnswerController
from src.answers.infrastructure.controllers.GetAllAnswersController import GetAllAnswersController
from src.answers.infrastructure.controllers.GetAnswerByIdController import GetAnswerByIdController
from src.answers.infrastructure.controllers.GetAnswersByResponseController import GetAnswersByResponseController
from src.answers.infrastructure.controllers.GetAnswersByQuestionController import GetAnswersByQuestionController
from src.answers.infrastructure.controllers.UpdateAnswerController import UpdateAnswerController
from src.answers.infrastructure.controllers.DeleteAnswerController import DeleteAnswerController


class AnswerDependencies:
    def __init__(
        self,
        create_answer_controller: CreateAnswerController,
        get_all_answers_controller: GetAllAnswersController,
        get_answer_by_id_controller: GetAnswerByIdController,
        get_answers_by_response_controller: GetAnswersByResponseController,
        get_answers_by_question_controller: GetAnswersByQuestionController,
        update_answer_controller: UpdateAnswerController,
        delete_answer_controller: DeleteAnswerController
    ):
        self.create_answer_controller = create_answer_controller
        self.get_all_answers_controller = get_all_answers_controller
        self.get_answer_by_id_controller = get_answer_by_id_controller
        self.get_answers_by_response_controller = get_answers_by_response_controller
        self.get_answers_by_question_controller = get_answers_by_question_controller
        self.update_answer_controller = update_answer_controller
        self.delete_answer_controller = delete_answer_controller


def init_answers(conn: MySQLConnection) -> AnswerDependencies:
    answer_repository = PostgreSQLAnswerRepository(conn)

    create_answer_use_case = CreateAnswerUseCase(answer_repository)
    get_all_answers_use_case = GetAllAnswersUseCase(answer_repository)
    get_answer_by_id_use_case = GetAnswerByIdUseCase(answer_repository)
    get_answers_by_response_use_case = GetAnswersByResponseUseCase(answer_repository)
    get_answers_by_question_use_case = GetAnswersByQuestionUseCase(answer_repository)
    update_answer_use_case = UpdateAnswerUseCase(answer_repository)
    delete_answer_use_case = DeleteAnswerUseCase(answer_repository)

    return AnswerDependencies(
        create_answer_controller=CreateAnswerController(create_answer_use_case),
        get_all_answers_controller=GetAllAnswersController(get_all_answers_use_case),
        get_answer_by_id_controller=GetAnswerByIdController(get_answer_by_id_use_case),
        get_answers_by_response_controller=GetAnswersByResponseController(get_answers_by_response_use_case),
        get_answers_by_question_controller=GetAnswersByQuestionController(get_answers_by_question_use_case),
        update_answer_controller=UpdateAnswerController(
            update_answer_use_case,
            get_answer_by_id_use_case
        ),
        delete_answer_controller=DeleteAnswerController(delete_answer_use_case)
    )