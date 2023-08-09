"""
Transaction module. This module contains handlers related
to transaction create, read, update and delete.
"""

from typing import Any, Optional

from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from loguru import logger
from sqlalchemy.orm import Session

from app import crud
from app.auth.bearer import JWTBearer
from app.db.session import db_connection
from app.schemas import (
    CreateTransaction,
    CreateTransactionResponse,
    DeleteTransactionResponse,
    GetTransactionResponse,
    UpdateTransaction,
    UpdateTransactionResponse,
)
from app.utils.exceptions import InvalidUUIDError
from app.utils.general import General
from app.utils.handle_error import handle_error
from app.utils.uuid_validation import is_valid_uuid

router = APIRouter()


@router.post(
    "/{portfolio_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=CreateTransactionResponse,
    response_model_exclude_unset=True,
)
async def create_transaction(
    portfolio_id: str,
    payload: CreateTransaction,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Creates a new transaction based on the given transaction details via payload.
    """

    try:
        if not is_valid_uuid(portfolio_id):
            raise InvalidUUIDError(
                "Invalid UUID format for user uuid",
                status_code=400,
            )
        if not crud.portfolio.get_by_portfolio_id(db, portfolio_id):
            raise InvalidUUIDError(
                "Invalid portfolio uuid",
                status_code=400,
            )
        payload.portfolio_id = portfolio_id
        transaction = General.exclude_metadata(
            jsonable_encoder(crud.transaction.create(db, payload))
        )

        return {
            "status": True,
            "message": "Successfully created the Transaction!",
            "details": transaction,
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.get(
    "/{portfolio_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=GetTransactionResponse,
    response_model_exclude_unset=True,
)
async def get_transaction(
    portfolio_id: str,
    response: Response,
    transaction_id: Optional[str] = None,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Gets transaction details.
    """

    try:
        if not is_valid_uuid(portfolio_id):
            raise InvalidUUIDError(
                "Invalid UUID format for user uuid",
                status_code=400,
            )
        if transaction_id:
            if not is_valid_uuid(transaction_id):
                raise InvalidUUIDError(
                    "Invalid UUID format for transaction uuid",
                    status_code=400,
                )
            if transaction := General.exclude_metadata(
                jsonable_encoder(
                    crud.transaction.get_by_transaction_id(db, transaction_id)
                )
            ):
                return {
                    "status": True,
                    "message": "Transaction Found!",
                    "details": transaction,
                }
            return {"status": False, "message": "Transaction Not Found!"}
        if transactions := General.exclude_metadata(
            jsonable_encoder(crud.transaction.get_by_portfolio_id(db, portfolio_id))
        ):
            return {
                "status": True,
                "message": "All Transactions Found!",
                "details": transactions,
            }
        return {
            "status": False,
            "message": "Transaction Not Found!",
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.put(
    "/{transaction_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=UpdateTransactionResponse,
    response_model_exclude_unset=True,
)
async def update_transaction(
    transaction_id: str,
    payload: UpdateTransaction,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Updates a transaction details
    """

    try:
        if not is_valid_uuid(transaction_id):
            raise InvalidUUIDError(
                "Invalid UUID format for transaction uuid",
                status_code=400,
            )
        if payload.portfolio_id:
            if not is_valid_uuid(payload.portfolio_id):
                raise InvalidUUIDError(
                    "Invalid UUID format for portfolio uuid",
                    status_code=400,
                )
            if not crud.portfolio.get_by_portfolio_id(db, payload.portfolio_id):
                raise InvalidUUIDError("Invalid Asset uuid", status_code=400)
        if payload.asset_id:
            if not is_valid_uuid(payload.asset_id):
                raise InvalidUUIDError(
                    "Invalid UUID format for asset uuid",
                    status_code=400,
                )
            if not crud.assets.get_by_asset_id(db, payload.asset_id):
                raise InvalidUUIDError("Invalid Portfolio uuid", status_code=400)
        payload.transaction_id = transaction_id
        if transaction := General.exclude_metadata(
            jsonable_encoder(crud.transaction.update(db, transaction_id, payload))
        ):
            return {
                "status": True,
                "message": "Successfully updated the transaction details!",
                "details": transaction,
            }

        return {
            "status": False,
            "message": "Transaction Not Found!",
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.delete(
    "/{transaction_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=DeleteTransactionResponse,
    response_model_exclude_unset=True,
)
async def delete_transaction(
    transaction_id: str,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Deletes a transaction details.
    """

    try:
        if not is_valid_uuid(transaction_id):
            raise InvalidUUIDError(
                "Invalid UUID format for portfolio uuid",
                status_code=400,
            )
        if not is_valid_uuid(transaction_id):
            raise InvalidUUIDError(
                "Invalid UUID format for transaction uuid",
                status_code=400,
            )
        transaction = crud.transaction.get_by_transaction_id(db, transaction_id)
        if transaction:
            if transaction := crud.transaction.delete(db, transaction_id):
                return {
                    "status": True,
                    "message": "Successfully deleted the transaction!",
                }

        return {
            "status": False,
            "message": "Transaction Not Found!",
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.get(
    "/user/{user_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=GetTransactionResponse,
    response_model_exclude_unset=True,
)
async def get_all_transactions(
    user_id: str,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Gets all transactions' details for a user.
    """
    try:
        if not is_valid_uuid(user_id):
            raise InvalidUUIDError(
                "Invalid UUID format for user uuid",
                status_code=400,
            )
        if not crud.user.get_by_user_id(db, user_id):
            raise InvalidUUIDError(
                "Invalid user uuid",
                status_code=400,
            )
        if portfolios := General.exclude_metadata(
            jsonable_encoder(crud.portfolio.get_by_user_id(db, user_id))
        ):
            all_transactions = []
            for portfolio in portfolios:
                if transactions := General.exclude_metadata(
                    jsonable_encoder(
                        crud.transaction.get_by_portfolio_id(
                            db, portfolio["portfolio_id"]
                        )
                    )
                ):
                    for transaction in transactions:
                        transaction["portfolio_name"] = portfolio["name"]
                        asset = General.exclude_metadata(
                            jsonable_encoder(
                                crud.assets.get_by_asset_id(db, transaction["asset_id"])
                            )
                        )
                        transaction["asset_name"] = asset["name"]
                    all_transactions += transactions
                return {
                    "status": True,
                    "message": "All Transactions Found!",
                    "details": all_transactions,
                }
        return {
            "status": True,
            "message": "No Portfolio Found!",
            "details": {},
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)
