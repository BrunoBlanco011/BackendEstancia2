from src.core.db_postgresql import MySQLConnection
from src.files.infrastructure.adapters.PostgreSQLFileRepository import PostgreSQLFileRepository
from src.files.application.CreateFileUseCase import CreateFileUseCase
from src.files.application.GetAllFilesUseCase import GetAllFilesUseCase
from src.files.application.GetFileByIdUseCase import GetFileByIdUseCase
from src.files.application.GetFilesByUserUseCase import GetFilesByUserUseCase
from src.files.application.DeleteFileUseCase import DeleteFileUseCase
from src.files.infrastructure.controllers.CreateFileController import CreateFileController
from src.files.infrastructure.controllers.GetAllFilesController import GetAllFilesController
from src.files.infrastructure.controllers.GetFileByIdController import GetFileByIdController
from src.files.infrastructure.controllers.GetFilesByUserController import GetFilesByUserController
from src.files.infrastructure.controllers.DeleteFileController import DeleteFileController


class FileDependencies:
    def __init__(
        self,
        create_file_controller: CreateFileController,
        get_all_files_controller: GetAllFilesController,
        get_file_by_id_controller: GetFileByIdController,
        get_files_by_user_controller: GetFilesByUserController,
        delete_file_controller: DeleteFileController
    ):
        self.create_file_controller = create_file_controller
        self.get_all_files_controller = get_all_files_controller
        self.get_file_by_id_controller = get_file_by_id_controller
        self.get_files_by_user_controller = get_files_by_user_controller
        self.delete_file_controller = delete_file_controller


def init_files(conn: MySQLConnection) -> FileDependencies:
    file_repository = PostgreSQLFileRepository(conn)

    create_file_use_case = CreateFileUseCase(file_repository)
    get_all_files_use_case = GetAllFilesUseCase(file_repository)
    get_file_by_id_use_case = GetFileByIdUseCase(file_repository)
    get_files_by_user_use_case = GetFilesByUserUseCase(file_repository)
    delete_file_use_case = DeleteFileUseCase(file_repository)

    return FileDependencies(
        create_file_controller=CreateFileController(create_file_use_case),
        get_all_files_controller=GetAllFilesController(get_all_files_use_case),
        get_file_by_id_controller=GetFileByIdController(get_file_by_id_use_case),
        get_files_by_user_controller=GetFilesByUserController(get_files_by_user_use_case),
        delete_file_controller=DeleteFileController(
            delete_file_use_case,
            get_file_by_id_use_case
        )
    )