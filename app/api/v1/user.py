"""
User module. This module contains handlers related
to user signup, login, and update details.
"""

from typing import Any

from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from loguru import logger
from sqlalchemy.orm import Session

from app import crud
from app.auth.auth import generate_token, is_valid_user, verify_gty
from app.auth.bearer import JWTBearer
from app.db.session import db_connection
from app.models.user import User
from app.schemas.user import (
    CreateUser,
    CreateUserResponse,
    GetUserResponse,
    SignInUser,
    SignInUserResponse,
    UpdateUser,
    UpdateUserResponse,
)
from app.utils import handle_error
from app.utils.exceptions import (
    CustomAuthError,
    CustomTokenError,
    DatabaseOperationError,
    InvalidUUIDError,
    SQLAlchemyObjectNotFoundError,
)
from app.utils.general import General
from app.utils.uuid_validation import is_valid_uuid

router = APIRouter()


@router.post(
    "/signup",
    response_model=CreateUserResponse,
    status_code=201,
    response_model_exclude_unset=True,
)
async def create_user(
    payload: CreateUser,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    User signup handler
    Creates a new user based on the given user details via payload.
    """

    try:
        if isinstance(payload, dict):
            data_in = payload
        else:
            data_in = payload.dict(exclude_unset=True)

        crud.user.create(db, data_in)

        return {
            "status": True,
            "message": "Successfully created the user!",
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.post(
    "/signin", response_model=SignInUserResponse, response_model_exclude_unset=True
)
async def signin(
    payload: SignInUser,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Signs in and grants access token for the given user in the payload
    """
    try:
        if isinstance(payload, dict):
            credentials_in = payload
        else:
            credentials_in = payload.dict(exclude_unset=True)

        email = credentials_in["email"]
        password = credentials_in["password"]

        valid_user = is_valid_user(db, email, password, User)

        if valid_user["status"]:
            access_token = generate_token(payload)
            user_details = General.exclude_metadata(
                jsonable_encoder(crud.user.get_by_email(db, email))
            )

            return {
                "status": True,
                "message": "Successfully signed in!",
                "details": {
                    "user_id": user_details["user_id"],
                    "access_token": access_token,
                },
            }

        # user not found in the database due to invalid/incorrect email
        if valid_user["error"] == "not_found":
            raise SQLAlchemyObjectNotFoundError(f"User with email `{email}` not found!")

        # inactive user.
        if valid_user["error"] == "inactive_user":
            raise CustomAuthError("Inactive user!", status_code=400)

        # invalid/incorrect password
        if valid_user["error"] == "invalid_pw":
            raise CustomAuthError("Incorrect/Invalid password!", status_code=400)

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.get(
    "/{user_id}/details",
    dependencies=[Depends(JWTBearer())],
    response_model=GetUserResponse,
    response_model_exclude_unset=True,
)
async def get_user_details(
    user_id: str,
    request: Request,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Returns details of the given user if found.
    """

    try:
        if not is_valid_uuid(user_id):
            raise InvalidUUIDError(
                "Make sure to provide user uuid in a valid UUID format.",
                status_code=400,
            )

        user_details = General.exclude_metadata(
            jsonable_encoder(verify_gty(db, request, User, user_id))
        )

        if user_details["status"]:
            return {
                "status": True,
                "message": "User details found",
                "details": {
                    # signup info
                    "user_id": user_details["user_id"],
                    "full_name": user_details["full_name"],
                    "email": user_details["email"],
                    "is_active": user_details["is_active"],
                },
            }

        # user tries to access someone else's details or
        # tampered with the token
        if user_details["error"] == "compromised":
            raise CustomAuthError(
                "You are not authorized to view this user details!",
                status_code=401,
            )

        # user not found the database
        if user_details["error"] == "not_found":
            raise SQLAlchemyObjectNotFoundError(f"User: `{user_id}` not found!")

        # invalid/incorrect JWT
        if user_details["error"] == "bad_request":
            raise CustomTokenError(
                "Make sure JWT/user id is sent correctly!", status_code=400
            )

        # Invalid signature or trying to access other user's
        # details than the user itself.
        # ---------------------------------------------------
        raise CustomAuthError(
            "You are not authorized to view this user details.", status_code=401
        )

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.put(
    "/{user_id}/updates",
    dependencies=[Depends(JWTBearer())],
    response_model=UpdateUserResponse,
    response_model_exclude_unset=True,
)
async def update_user_details(
    user_id: str,
    payload: UpdateUser,
    request: Request,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Updates a user details
    """

    try:
        if not is_valid_uuid(user_id):
            raise InvalidUUIDError(
                "Make sure to provide user uuid in a valid UUID format.",
                status_code=400,
            )

        user_details = verify_gty(db, request, User, user_id)

        if user_details["status"]:
            update_details = jsonable_encoder(crud.user.update(db, user_id, payload))
            update_details = General.exclude_metadata(update_details)

            if update_details:
                return {
                    "status": True,
                    "message": "Successfully updated the user!",
                    "details": update_details,
                }
            # fixme: check what are possible errors and pass the error message accordingly.
            raise DatabaseOperationError("Database operation error")

        raise CustomAuthError(
            "You are unauthorized to update this user details.",
            status_code=401,
        )

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.delete(
    "/{user_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=UpdateUserResponse,
    response_model_exclude_unset=True,
)
async def delete_a_user(
    user_id: str,
    request: Request,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Deletes a user.
    """

    try:
        if not is_valid_uuid(user_id):
            raise InvalidUUIDError(
                "Make sure to provide user uuid in a valid UUID format.",
                status_code=400,
            )

        user_details = verify_gty(db, request, User, user_id)

        if user_details["status"]:
            user_details = crud.user.delete(db, user_id)
            if user_details:
                return {"status": True, "message": "Successfully deleted the user!"}

        raise CustomAuthError(
            "You are unauthorized to delete this user details.", status_code=401
        )

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)
