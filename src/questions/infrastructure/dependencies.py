from src.core.db_postgresql import MySQLConnection
from src.questions.infrastructure.adapters.PostgreSQLQuestionRepository import PostgreSQLQuestionRepository
from src.questions.application.CreateQuestionUseCase import CreateQuestionUseCase
from src.questions.application.GetAllQuestionsUseCase import GetAllQuestionsUseCase
from src.questions.application.GetQuestionByIdUseCase import GetQuestionByIdUseCase
from src.questions.application.GetQuestionsBySurveyUseCase import GetQuestionsBySurveyUseCase
from src.questions.application.UpdateQuestionUseCase import UpdateQuestionUseCase
from src.questions.application.DeleteQuestionUseCase import DeleteQuestionUseCase
from src.questions.infrastructure.controllers.CreateQuestionController import CreateQuestionController
from src.questions.infrastructure.controllers.GetAllQuestionsController import GetAllQuestionsController
from src.questions.infrastructure.controllers.GetQuestionByIdController import GetQuestionByIdController
from src.questions.infrastructure.controllers.GetQuestionsBySurveyController import GetQuestionsBySurveyController
from src.questions.infrastructure.controllers.UpdateQuestionController import UpdateQuestionController
from src.questions.infrastructure.controllers.DeleteQuestionController import DeleteQuestionController


class QuestionDependencies:
    def __init__(
        self,
        create_question_controller: CreateQuestionController,
        get_all_questions_controller: GetAllQuestionsController,
        get_question_by_id_controller: GetQuestionByIdController,
        get_questions_by_survey_controller: GetQuestionsBySurveyController,
        update_question_controller: UpdateQuestionController,
        delete_question_controller: DeleteQuestionController
    ):
        self.create_question_controller = create_question_controller
        self.get_all_questions_controller = get_all_questions_controller
        self.get_question_by_id_controller = get_question_by_id_controller
        self.get_questions_by_survey_controller = get_questions_by_survey_controller
        self.update_question_controller = update_question_controller
        self.delete_question_controller = delete_question_controller


def init_questions(conn: MySQLConnection) -> QuestionDependencies:
    question_repository = PostgreSQLQuestionRepository(conn)

    create_question_use_case = CreateQuestionUseCase(question_repository)
    get_all_questions_use_case = GetAllQuestionsUseCase(question_repository)
    get_question_by_id_use_case = GetQuestionByIdUseCase(question_repository)
    get_questions_by_survey_use_case = GetQuestionsBySurveyUseCase(question_repository)
    update_question_use_case = UpdateQuestionUseCase(question_repository)
    delete_question_use_case = DeleteQuestionUseCase(question_repository)

    return QuestionDependencies(
        create_question_controller=CreateQuestionController(create_question_use_case),
        get_all_questions_controller=GetAllQuestionsController(get_all_questions_use_case),
        get_question_by_id_controller=GetQuestionByIdController(get_question_by_id_use_case),
        get_questions_by_survey_controller=GetQuestionsBySurveyController(get_questions_by_survey_use_case),
        update_question_controller=UpdateQuestionController(
            update_question_use_case,
            get_question_by_id_use_case
        ),
        delete_question_controller=DeleteQuestionController(delete_question_use_case)
    )