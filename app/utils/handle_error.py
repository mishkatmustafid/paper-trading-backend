"""
Custom error handling module
"""

from fastapi import Response
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.utils.exceptions import (
    CustomAuthError,
    CustomTokenError,
    CustomTransferError,
    DatabaseOperationError,
    InvalidUUIDError,
    SQLAlchemyObjectNotFoundError,
    PaperTradeCustomError,
)

# psycopg2.errors.NotNullViolation


class HandleError(PaperTradeCustomError):
    """
    Class for handing custom errors.
    """

    # pylint: disable=too-many-return-statements

    @classmethod
    def send_error(cls, error: PaperTradeCustomError, response: Response):
        """
        Sends corresponding error message back to the caller based
        on the error instance.
        """

        if isinstance(error, IntegrityError):
            logger.error(f"IntegrityError: {error}")
            response.status_code = 400
            return {
                "status": False,
                "message": "Duplicate key value violates unique constraint",
            }

        if isinstance(error, SQLAlchemyObjectNotFoundError):
            logger.error(f"SQLAlchemyObjectNotFoundError: {error.message}")
            response.status_code = 404
            return {
                "status": False,
                "message": f"{error.message}",
            }

        if isinstance(error, ValidationError):
            logger.error(f"ValidationError: {error}")
            response.status_code = 422
            return {"status": False, "message": error.message}

        if isinstance(error, ValueError):
            logger.error(f"ValueError: {error}")
            response.status_code = 400
            return {"status": False, "message": "Bad value"}

        if isinstance(error, TimeoutError):
            response.status_code = 504
            logger.error(f"TimeoutError: {error}")
            return {"status": False, "message": "Request timed out"}

        if isinstance(error, CustomAuthError):
            logger.error(f"CustomAuthError: {error}")
            if error.status_code:
                response.status_code = error.status_code
                return {
                    "status": False,
                    "message": error.message,
                }
            response.status_code = 401
            return {
                "status": False,
                "message": error.message,
            }

        # pylint: disable=fixme
        # fixme: check possible database errors and log message accordingly.
        if isinstance(error, DatabaseOperationError):
            logger.error(f"DatabaseOperationError: {error}")
            response.status_code = 400
            return {"status": False, "message": error.message}

        if isinstance(error, CustomTokenError):
            logger.error(f"CustomTokenError: {error}")
            response.status_code = 400
            return {
                "status": False,
                "message": "Make sure to provide data in a valid JSON format!",
            }

        if isinstance(error, InvalidUUIDError):
            logger.error(f"InvalidUUIDError: {error}")
            response.status_code = 400
            return {"status": False, "message": error.message}

        if isinstance(error, CustomTransferError):
            logger.error(f"CustomTransferError: {error}")
            response.status_code = 406
            return {"status": False, "message": error.message}

        response.status_code = 500
        return {"status": False, "message": str(error)}


handle_error = HandleError()
