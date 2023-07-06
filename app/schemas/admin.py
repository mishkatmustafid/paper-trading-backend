# """
# Admin user schema module
# """
# from typing import Optional

# from pydantic import BaseModel, EmailStr, Field

# from app.models.admin_level import AdminLevel


# # Shared properties
# class BaseAdminUser(BaseModel):
#     full_name: Optional[str] = None
#     email: Optional[EmailStr] = None
#     username: Optional[str] = None


# # Shared response properties
# class BaseAdminUserResponse(BaseModel):
#     status: Optional[bool] = True
#     message: Optional[str] = None


# # Properties to receive via API on creation
# class CreateAdminUser(BaseAdminUser):
#     """
#     Schema class for creating admin user
#     """

#     full_name: str
#     email: EmailStr
#     username: str
#     password: str
#     admin_level: AdminLevel

#     class Config:
#         schema_extra = {
#             "example": {
#                 "full_name": "Admin User",
#                 "email": "admin@tigertrade.live",
#                 "username": "admin",
#                 "password": "AdminPass!",
#                 "admin_level": 5,
#             }
#         }


# class CreateAdminUserResponse(BaseAdminUserResponse):
#     status: bool
#     message: str

#     class Config:
#         schema_extra = {
#             "example": {
#                 "status": True,
#                 "message": "New admin/api user created Successfully!",
#             }
#         }


# class SignInAdminUser(BaseAdminUser):
#     email: str = Field(...)
#     password: str = Field(...)

#     class Config:
#         schema_extra = {
#             "example": {"email": "admin@tigertrade.live", "password": "AdminPass!"}
#         }


# class SignInAdminUserResponse(BaseAdminUserResponse):
#     details: Optional[dict] = None

#     class Config:
#         orm_mode = True

#         # pylint: disable=line-too-long
#         schema_extra = {
#             "example": {
#                 "status": True,
#                 "message": "Successfully signed in!",
#                 "details": {
#                     "user_id": "b0f63ec3-d721-4289-92a6-1ff92a8a5cda",
#                     "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpcMdcpiJsb2NhbGhvc3QiLCJpYXQiOjE2MzYwMTUwNzgsImV4cCI6MTYzNjAxNjg3OCwiYXVkIjoiZW1haWxAc2h1bW9uLm1lIn0.0slVFU_INXv13X4yQAvW1VCNJI6XUu5qOP6aPXD03VM",
#                 },
#             }
#         }


# class GetAdminUserResponse(BaseAdminUserResponse):
#     details: Optional[dict] = None

#     class Config:
#         orm_mode = True

#         schema_extra = {
#             "example": {
#                 "status": True,
#                 "message": "User Details found!",
#                 "details": {
#                     "full_name": "Admin User",
#                     "email": "admin@tigertrade.live",
#                     "username": "admin",
#                     "status": True,
#                 },
#             }
#         }


# class UpdateAdminUser(BaseAdminUser):
#     """
#     User update schema. Properties to receive via API on update
#     """

#     password: Optional[str] = None


# class UpdateAdminUserResponse(BaseAdminUserResponse):
#     details: Optional[dict] = None

#     class Config:
#         schema_extra = {
#             "example": {
#                 "status": True,
#                 "message": "Successfully updated the user details!",
#                 "details": {
#                     "full_name": "Admin User",
#                     "email:": "admin@tigertrade.live",
#                     "username": "admin",
#                 },
#             }
#         }


# class DeleteAdminUserResponse(BaseAdminUserResponse):
#     class Config:
#         schema_extra = {
#             "example": {
#                 "status": True,
#                 "message": "Successfully deleted the admin user!",
#             }
#         }


# # Properties to receive via API on update
# class AdminUserUpdate(BaseAdminUser):
#     password: Optional[str] = None
