from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100, alias="lastName")
    email: EmailStr
    password: str = Field(..., min_length=6)
    role_id: int = Field(..., ge=1, alias="roleId")
    profile_image: Optional[str] = Field(None, max_length=500, alias="profileImage")

    class Config:
        populate_by_name = True


class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, alias="lastName")
    email: Optional[EmailStr] = None
    profile_image: Optional[str] = Field(None, max_length=500, alias="profileImage")

    class Config:
        populate_by_name = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str