from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.core.db_postgresql import get_db_connection
from src.users.infrastructure.dependencies import init_users
from src.users.infrastructure.routes.Routes import configure_user_routes
from src.survey.infrastructure.dependencies import init_surveys
from src.survey.infrastructure.routes.Routes import configure_survey_routes
from src.questions.infrastructure.dependencies import init_questions
from src.questions.infrastructure.routes.Routes import configure_question_routes
from src.question_options.infrastructure.dependencies import init_question_options
from src.question_options.infrastructure.routes.Routes import configure_question_option_routes
from src.responses.infrastructure.dependencies import init_responses
from src.responses.infrastructure.routes.Routes import configure_response_routes
from src.answers.infrastructure.dependencies import init_answers
from src.answers.infrastructure.routes.Routes import configure_answer_routes
from src.answer_options.infrastructure.dependencies import init_answer_options
from src.answer_options.infrastructure.routes.Routes import configure_answer_option_routes
from src.files.infrastructure.dependencies import init_files
from src.files.infrastructure.routes.Routes import configure_file_routes
from src.nlp.infrastructure.dependencies import init_nlp
from src.nlp.infrastructure.routes.Routes import configure_nlp_routes
from fastapi import APIRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando servidor...")
    db_connection = get_db_connection()
    yield
    print("Cerrando conexiones...")
    db_connection.close()

app = FastAPI(
    title="Api para encuestas",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_connection = get_db_connection()

user_dependencies = init_users(db_connection)
survey_dependencies = init_surveys(db_connection)
question_dependencies = init_questions(db_connection)
question_option_dependencies = init_question_options(db_connection)
response_dependencies = init_responses(db_connection)
answer_dependencies = init_answers(db_connection)
answer_option_dependencies = init_answer_options(db_connection)
file_dependencies = init_files(db_connection)
nlp_dependencies = init_nlp()

api_router = APIRouter(prefix="/api")

configure_user_routes(
    api_router,
    user_dependencies.create_user_controller,
    user_dependencies.get_all_users_controller,
    user_dependencies.get_by_id_user_controller,
    user_dependencies.update_user_controller,
    user_dependencies.delete_user_controller,
    user_dependencies.auth_controller
)

configure_survey_routes(
    api_router,
    survey_dependencies.create_survey_controller,
    survey_dependencies.get_all_surveys_controller,
    survey_dependencies.get_survey_by_id_controller,
    survey_dependencies.get_surveys_by_user_controller,
    survey_dependencies.update_survey_controller,
    survey_dependencies.delete_survey_controller
)

configure_question_routes(
    api_router,
    question_dependencies.create_question_controller,
    question_dependencies.get_all_questions_controller,
    question_dependencies.get_question_by_id_controller,
    question_dependencies.get_questions_by_survey_controller,
    question_dependencies.update_question_controller,
    question_dependencies.delete_question_controller
)

configure_question_option_routes(
    api_router,
    question_option_dependencies.create_option_controller,
    question_option_dependencies.get_all_options_controller,
    question_option_dependencies.get_option_by_id_controller,
    question_option_dependencies.get_options_by_question_controller,
    question_option_dependencies.update_option_controller,
    question_option_dependencies.delete_option_controller
)

configure_response_routes(
    api_router,
    response_dependencies.create_response_controller,
    response_dependencies.get_all_responses_controller,
    response_dependencies.get_response_by_id_controller,
    response_dependencies.get_responses_by_survey_controller,
    response_dependencies.get_responses_by_user_controller,
    response_dependencies.delete_response_controller
)

configure_answer_routes(
    api_router,
    answer_dependencies.create_answer_controller,
    answer_dependencies.get_all_answers_controller,
    answer_dependencies.get_answer_by_id_controller,
    answer_dependencies.get_answers_by_response_controller,
    answer_dependencies.get_answers_by_question_controller,
    answer_dependencies.update_answer_controller,
    answer_dependencies.delete_answer_controller
)

configure_answer_option_routes(
    api_router,
    answer_option_dependencies.create_answer_option_controller,
    answer_option_dependencies.get_all_answer_options_controller,
    answer_option_dependencies.get_answer_option_by_id_controller,
    answer_option_dependencies.get_answer_options_by_answer_controller,
    answer_option_dependencies.delete_answer_option_controller
)

configure_file_routes(
    api_router,
    file_dependencies.create_file_controller,
    file_dependencies.get_all_files_controller,
    file_dependencies.get_file_by_id_controller,
    file_dependencies.get_files_by_user_controller,
    file_dependencies.delete_file_controller
)

configure_nlp_routes(
    api_router,
    nlp_dependencies.extract_keywords,
    nlp_dependencies.extract_and_rank_keywords,
    nlp_dependencies.extract_phrases
)

app.include_router(api_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "transcriptor-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)