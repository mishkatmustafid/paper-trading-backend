"""
User schema module
"""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.profile_status import ProfileStatus


class UserBase(BaseModel):
    """
    Base user class. This class holds all the possible attributes of a user.
    """

    id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True
    profile_status: Optional[ProfileStatus] = "SIGNUP"


class CreateUser(UserBase):
    """
    User create schema. Properties to receive via API on creation
    """

    full_name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "full_name": "Some User",
                "email": "user@papertrade.live",
                "password": "nopassword",
            }
        }


class CreateUserResponse(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully created the user!",
                "details": {
                    "user_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "full_name": "Some User",
                    "email": "user@papertrade.live",
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpcMdcpiJsb2NhbGhvc3QiLCJpYXQiOjE2MzYwMTUwNzgsImV4cCI6MTYzNjAxNjg3OCwiYXVkIjoiZW1haWxAc2h1bW9uLm1lIn0.0slVFU_INXv13X4yQAvW1VCNJI6XUu5qOP6aPXD03VM",
                },
            }
        }


class GetUserResponse(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None
    details: Optional[dict] = None

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "status": True,
                "message": "Details found!",
                "details": {
                    "full_name": "Some User",
                    "email": "user@papertrade.live",
                },
            }
        }


class SignInUser(UserBase):
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "user@papertrade.live",
                "password": "nopassword",
            }
        }


class SignInUserResponse(BaseModel):
    status: bool
    message: str
    details: Optional[dict] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully signed in!",
                "details": {
                    "user_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpcMdcpiJsb2NhbGhvc3QiLCJpYXQiOjE2MzYwMTUwNzgsImV4cCI6MTYzNjAxNjg3OCwiYXVkIjoiZW1haWxAc2h1bW9uLm1lIn0.0slVFU_INXv13X4yQAvW1VCNJI6XUu5qOP6aPXD03VM",
                },
            }
        }


class GetAllUsersResponse(BaseModel):
    status: bool
    message: str
    users: Optional[list] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "status": True,
                "message": "All users found!",
                "users": [
                    {
                        "fullname": "Paper trade",
                        "email:": "info@gmail.com",
                        "username": "someuser",
                    }
                ],
            }
        }


class UpdateUser(UserBase):
    """
    User update schema. Properties to receive via API on update
    """

    password: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "full_name": "John Doe",
            }
        }


class UpdateUserResponse(BaseModel):
    status: bool
    message: str
    details: dict = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully updated the user!",
                "details": {
                    "full_name": "Paper trade",
                    "email:": "info@gmail.com",
                },
            }
        }
