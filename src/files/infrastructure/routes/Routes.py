from fastapi import APIRouter, Path, UploadFile, File, Form
from src.files.infrastructure.controllers.CreateFileController import CreateFileController
from src.files.infrastructure.controllers.GetAllFilesController import GetAllFilesController
from src.files.infrastructure.controllers.GetFileByIdController import GetFileByIdController
from src.files.infrastructure.controllers.GetFilesByUserController import GetFilesByUserController
from src.files.infrastructure.controllers.DeleteFileController import DeleteFileController


def configure_file_routes(
    router: APIRouter,
    create_file_controller: CreateFileController,
    get_all_files_controller: GetAllFilesController,
    get_file_by_id_controller: GetFileByIdController,
    get_files_by_user_controller: GetFilesByUserController,
    delete_file_controller: DeleteFileController
):
    @router.post("/files")
    async def create_file(
        uploaded_by: int = Form(..., alias="uploadedBy"),
        file: UploadFile = File(...)
    ):
        return await create_file_controller.execute(uploaded_by, file)

    @router.get("/files")
    async def get_all_files():
        return await get_all_files_controller.execute()

    @router.get("/files/{file_id}")
    async def get_file_by_id(file_id: int = Path(..., gt=0)):
        return await get_file_by_id_controller.execute(file_id)

    @router.get("/users/{user_id}/files")
    async def get_files_by_user(user_id: int = Path(..., gt=0)):
        return await get_files_by_user_controller.execute(user_id)

    @router.delete("/files/{file_id}")
    async def delete_file(file_id: int = Path(..., gt=0)):
        return await delete_file_controller.execute(file_id)