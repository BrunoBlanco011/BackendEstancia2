from pydantic import BaseModel
from typing import Optional, List
import os

class UserResponse(BaseModel):
    id: Optional[int]
    name: str
    last_name: str
    email: str
    role_id: int
    registration_date: str
    profile_image_url: Optional[str]

    @staticmethod
    def from_user(user):
        profile_image_url = None
        if user.profile_image:
            cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
            profile_image_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/{user.profile_image}"

        return UserResponse(
            id=user.user_id,
            name=user.name,
            last_name=user.last_name,
            email=user.email,
            role_id=user.role_id,
            registration_date=user.registration_date.isoformat() if user.registration_date else "",
            profile_image_url=profile_image_url
        )


class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int


class SingleUserResponse(BaseModel):
    user: UserResponse


class CreatedUserData(BaseModel):
    userId: Optional[int]
    name: str
    lastName: str
    email: str
    registrationDate: str
    roleId: int
    profileImageUrl: Optional[str]


class CreateUserResponse(BaseModel):
    message: str
    user: CreatedUserData


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str


class LoginResponse(BaseModel):
    token: str
    userId: int
    roleId: int
    name: str
    email: str
    profileImageUrl: Optional[str]


class LoginSuccessResponse(BaseModel):
    message: str
    data: LoginResponse