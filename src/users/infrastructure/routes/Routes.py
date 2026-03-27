from fastapi import APIRouter, Path, UploadFile, File, Form
from src.users.infrastructure.controllers.CreateUserController import CreateUserController
from src.users.infrastructure.controllers.GetAllUsersController import GetAllUsersController
from src.users.infrastructure.controllers.GetUserByIdController import GetUserByIdController
from src.users.infrastructure.controllers.UpdateUserController import UpdateUserController
from src.users.infrastructure.controllers.DeleteUserController import DeleteUserController
from src.users.infrastructure.controllers.AuthController import AuthController
from src.users.domain.dto.UserRequest import LoginRequest
from typing import Optional


def configure_user_routes(
        router: APIRouter,
        create_user_controller: CreateUserController,
        get_all_users_controller: GetAllUsersController,
        get_by_id_user_controller: GetUserByIdController,
        update_user_controller: UpdateUserController,
        delete_user_controller: DeleteUserController,
        auth_controller: AuthController
):
    @router.post("/users")
    async def create_user(
            name: str = Form(...),
            lastName: str = Form(...),
            email: str = Form(...),
            password: str = Form(...),
            roleId: int = Form(...),
            profileImage: Optional[UploadFile] = File(None)
    ):
        return await create_user_controller.execute(
            name, lastName, email, password, roleId, profileImage
        )

    @router.get("/users")
    async def get_all_users():
        return await get_all_users_controller.execute()

    @router.get("/users/{user_id}")
    async def get_user_by_id(user_id: int = Path(..., gt=0)):
        return await get_by_id_user_controller.execute(user_id)

    @router.put("/users/{user_id}")
    async def update_user(
            user_id: int = Path(..., gt=0),
            name: Optional[str] = Form(None),
            lastName: Optional[str] = Form(None),
            email: Optional[str] = Form(None),
            profileImage: Optional[UploadFile] = File(None)
    ):
        return await update_user_controller.execute(
            user_id, name, lastName, email, profileImage
        )

    @router.delete("/users/{user_id}")
    async def delete_user(user_id: int = Path(..., gt=0)):
        return await delete_user_controller.execute(user_id)

    @router.post("/auth/login")
    async def login(request: LoginRequest):
        return await auth_controller.execute(request)