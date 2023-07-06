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
    DeleteTransaction,
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
    "/{portfolio_stock_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=CreateTransactionResponse,
    response_model_exclude_unset=True,
)
async def create_transaction(
    portfolio_stock_id: str,
    payload: CreateTransaction,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Creates a new transaction based on the given transaction details via payload.
    """

    try:
        if not is_valid_uuid(portfolio_stock_id):
            raise InvalidUUIDError(
                "Invalid UUID format for user uuid",
                status_code=400,
            )
        if not crud.portfolio_stock.get_by_portfolio_stock_id(db, portfolio_stock_id):
            raise InvalidUUIDError(
                "Invalid portfolio stock uuid",
                status_code=400,
            )
        payload.portfolio_stock_id = portfolio_stock_id
        transaction = General.exclude_metadata(
            jsonable_encoder(crud.transaction.create(db, payload))
        )

        return {
            "status": True,
            "message": "Successfully created the Transaction!",
            "details": {
                "transaction_id": transaction["transaction_id"],
                "portfolio_stock_id": portfolio_stock_id,
                "transaction_type": transaction["transaction_type"],
                "transaction_date": transaction["transaction_date"],
                "transaction_price": transaction["transaction_price"],
                "quantity": transaction["quantity"],
                "order_type": transaction["order_type"],
                "limit_price": transaction["limit_price"],
                "transaction_value": transaction["transaction_value"],
                "realized_profit_loss": transaction["realized_profit_loss"],
            },
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.get(
    "/{portfolio_stock_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=GetTransactionResponse,
    response_model_exclude_unset=True,
)
async def get_transaction(
    portfolio_stock_id: str,
    response: Response,
    transaction_id: Optional[str] = None,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Gets transaction details.
    """

    try:
        if not is_valid_uuid(portfolio_stock_id):
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
                    "details": {
                        "transaction_id": transaction["transaction_id"],
                        "portfolio_stock_id": portfolio_stock_id,
                        "transaction_type": transaction["transaction_type"],
                        "transaction_date": transaction["transaction_date"],
                        "transaction_price": transaction["transaction_price"],
                        "quantity": transaction["quantity"],
                        "order_type": transaction["order_type"],
                        "limit_price": transaction["limit_price"],
                        "transaction_value": transaction["transaction_value"],
                        "realized_profit_loss": transaction["realized_profit_loss"],
                    },
                }
            return {"status": False, "message": "Transaction Not Found!"}
        if transactions := General.exclude_metadata(
            jsonable_encoder(
                crud.transaction.get_by_portfolio_stock_id(db, portfolio_stock_id)
            )
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
    "/{portfolio_stock_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=UpdateTransactionResponse,
    response_model_exclude_unset=True,
)
async def update_transaction(
    portfolio_stock_id: str,
    payload: UpdateTransaction,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Updates a transaction details
    """

    try:
        if not is_valid_uuid(portfolio_stock_id):
            raise InvalidUUIDError(
                "Invalid UUID format for portfolio stock uuid",
                status_code=400,
            )
        if not is_valid_uuid(payload.transaction_id):
            raise InvalidUUIDError(
                "Invalid UUID format for transaction uuid",
                status_code=400,
            )
        payload.portfolio_stock_id = portfolio_stock_id
        if transaction := General.exclude_metadata(
            jsonable_encoder(
                crud.transaction.update(db, payload.transaction_id, payload)
            )
        ):
            details = payload.dict(exclude_unset=True)
            details["transaction_id"] = transaction["transaction_id"]
            return {
                "status": True,
                "message": "Successfully updated the transaction details!",
                "details": details,
            }

        return {
            "status": False,
            "message": "Transaction Not Found!",
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.delete(
    "/{portfolio_stock_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=DeleteTransactionResponse,
    response_model_exclude_unset=True,
)
async def delete_transaction(
    portfolio_stock_id: str,
    payload: DeleteTransaction,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Deletes a transaction details.
    """

    try:
        if not is_valid_uuid(portfolio_stock_id):
            raise InvalidUUIDError(
                "Invalid UUID format for portfolio stock uuid",
                status_code=400,
            )
        if not is_valid_uuid(payload.transaction_id):
            raise InvalidUUIDError(
                "Invalid UUID format for transaction uuid",
                status_code=400,
            )
        transaction = crud.transaction.get_by_transaction_id(db, payload.transaction_id)
        if transaction:
            if transaction := crud.transaction.delete(db, payload.transaction_id):
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
