from src.core.db_postgresql import MySQLConnection
from src.users.infrastructure.adapters.PostgreSQLUserRepository import PostgreSQLUserRepository
from src.users.application.CreateUserUseCase import CreateUserUseCase
from src.users.application.GetAllUsersUseCase import GetAllUsersUseCase
from src.users.application.GetUserByIdUseCase import GetUserByIdUseCase
from src.users.application.UpdateUserUseCase import UpdateUserUseCase
from src.users.application.DeleteUserUseCase import DeleteUserUseCase
from src.users.application.AuthUseCase import AuthUseCase
from src.users.infrastructure.controllers.CreateUserController import CreateUserController
from src.users.infrastructure.controllers.GetAllUsersController import GetAllUsersController
from src.users.infrastructure.controllers.GetUserByIdController import GetUserByIdController
from src.users.infrastructure.controllers.UpdateUserController import UpdateUserController
from src.users.infrastructure.controllers.DeleteUserController import DeleteUserController
from src.users.infrastructure.controllers.AuthController import AuthController

class UserDependencies:
    def __init__(
            self,
            create_user_controller: CreateUserController,
            get_all_users_controller: GetAllUsersController,
            get_by_id_user_controller: GetUserByIdController,
            update_user_controller: UpdateUserController,
            delete_user_controller: DeleteUserController,
            auth_controller: AuthController
    ):
        self.create_user_controller = create_user_controller
        self.get_all_users_controller = get_all_users_controller
        self.get_by_id_user_controller = get_by_id_user_controller
        self.update_user_controller = update_user_controller
        self.delete_user_controller = delete_user_controller
        self.auth_controller = auth_controller


def init_users(conn: MySQLConnection) -> UserDependencies:
    user_repository = PostgreSQLUserRepository(conn)

    auth_service = AuthUseCase(user_repository)
    create_user_use_case = CreateUserUseCase(user_repository)
    get_all_users_use_case = GetAllUsersUseCase(user_repository)
    get_user_by_id_use_case = GetUserByIdUseCase(user_repository)
    update_user_use_case = UpdateUserUseCase(user_repository)
    delete_user_use_case = DeleteUserUseCase(user_repository)

    return UserDependencies(
        create_user_controller=CreateUserController(create_user_use_case, auth_service, user_repository),
        get_all_users_controller=GetAllUsersController(get_all_users_use_case),
        get_by_id_user_controller=GetUserByIdController(get_user_by_id_use_case),
        update_user_controller=UpdateUserController(update_user_use_case),
        delete_user_controller=DeleteUserController(delete_user_use_case),
        auth_controller=AuthController(auth_service)
    )