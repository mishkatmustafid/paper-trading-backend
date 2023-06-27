import secrets
import time
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import jwt
from loguru import logger
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Any, Dict, Optional, Type, TypeVar
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError


from app.core import settings
from app.models.admin_level import AdminLevel
from app.models.base import Base
from app.models.user import User


security = HTTPBasic()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ModelType = TypeVar("ModelType", bound=Base)
Email = TypeVar("S")
Password = TypeVar("S")
UserId = TypeVar("S")
Model = Type[ModelType]


def is_valid_user(db: Session, email: Email, password: Password, model: Model) -> Dict:
    """
    Checks if a given email and password belongs a valid user.
    """
    current_user = jsonable_encoder(model.get_by_email(db, email))

    if current_user is not None:
        if verify_password(password, current_user["password"]):
            if current_user["is_active"]:
                return {"status": True}

            return {"status": False, "error": "inactive_user"}

        return {"status": False, "error": "invalid_pw"}

    return {"status": False, "error": "not_found"}


def is_valid_authorised_user(
    db: Session,
    credentials: HTTPBasicCredentials,
    model: Model,
    is_super_user: Optional[bool],
) -> bool:
    """
    Returns true if a given credentials are valid and api-username exists in the db.
    False otherwise.
    """
    query_result = jsonable_encoder(model.get_by_username(db, credentials.username))

    if query_result is not None and verify_password(
        credentials.password, query_result["password"]
    ):
        # > if is_super_user flag's true  that means we are checking
        # if given username is a super user (i.e. super admin) and is active
        # -----------------------------
        if is_super_user:
            return bool(
                query_result["is_active"]
                and AdminLevel.is_admin(query_result["admin_level"])
            )

        # > Password matched and is_super_user flag is false means
        # it's a valid api-user/general user
        # --------------------
        return True

    return False


def is_authenticated(username: str, password: str, db: Session) -> Dict:
    """
    Checks if the given user is authenticated.
    """
    current_user = jsonable_encoder(User.get_by_username(db, username))

    if current_user is not None:
        verified_password = verify_password(password, current_user["password"])

        if verified_password:
            return {"status": True}
        return {"status": False, "message": "Invalid password"}

    return {"status": False, "message": "User doesn't exists."}


def get_apidoc_username(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Returns apidoc username if credentials are valid.
    """
    correct_username = secrets.compare_digest(
        credentials.username, settings.BA_API_DOC_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.BA_API_DOC_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def encode_jwt(username: str, password: str) -> str:
    """Generates JWT"""

    # The JWT specification defines some registered claim names
    # and how they should be used. Following terms describe
    # what they stand for.
    # > iss: Issuer Claim
    # > iat: Issued At Claim
    # > exp: Expiration Time Claim
    # > aud: Audience Claim
    # Token is valid for 30 minutes. It can be set to shorter/longer
    # time depending on need.
    # ===========================

    payload = {
        "iss": settings.TOKEN_ISSUER,
        "iat": int(time.time()),
        "exp": datetime.utcnow() + timedelta(days=1, minutes=0),
        "aud": settings.TOKEN_AUDIENCE,
        "gty": f"{username}:{password}",
    }

    access_token = jwt.encode(
        payload, settings.SIGNING_KEY, algorithm=settings.SIGNING_ALGORITHM
    ).decode("utf-8")

    return access_token


def decode_jwt(token: str) -> Dict:  # pylint: disable=inconsistent-return-statements
    """
    Checks if a given jwt is valid. If it is
    then request is further allowed to access
    intended API.
    """

    try:
        decoded_token = jwt.decode(
            token,
            settings.SIGNING_KEY,
            algorithms=settings.SIGNING_ALGORITHM,
            issuer=settings.TOKEN_ISSUER,
            audience=settings.TOKEN_AUDIENCE,
        )

        if "exp" in decoded_token and decoded_token["exp"] >= time.time():
            return decoded_token

    except (DecodeError, ExpiredSignatureError, InvalidTokenError) as err:
        logger.error(f"DECODE_TOKEN_ERROR: {err}")
        return err


def generate_token(payload) -> str:
    return encode_jwt(payload.email, payload.password)


def verify_token(token: str) -> bool:
    return isinstance(decode_jwt(token), dict)


def hash_password(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def verify_gty(
    db: Session,
    request: Request,
    model: Model,
    user_id: UserId,
) -> Any:
    """
    Extracts bearer token from the header authorization
    and checks its validity.
    """
    try:
        auth_header = request.headers.get("authorization")

        # pylint: disable=unused-variable
        bearer, _, access_token = auth_header.partition(" ")

        decoded_token = decode_jwt(access_token)

        decoded_token = decoded_token["gty"].partition(":")
        user = jsonable_encoder(model.get_by_userid(db, user_id))

        if user is None:
            return jsonable_encoder({"status": False, "error": "not_found"})

        # user details are returned only when email and password of the decoded token
        # and the user_id matches with the extracted user details from the db.
        # If they don't match then it's safe to assume that user_id/token sent
        # is compromised/tampered with. Therefore unauthorised response is sent.
        # ------------------------------------------------------------------------
        if (
            user["email"] != decoded_token[0]
            or not verify_password(decoded_token[2], user["password"])
            or user["user_id"] != user_id
        ):
            return jsonable_encoder({"status": False, "error": "compromised"})

        user["status"] = True
        return user

    except Exception as err:
        return err
