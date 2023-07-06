"""
Transaction schema module
"""

import enum
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from app.models.order_type import OrderType
from app.models.transaction_type import TransactionType


class TransactionBase(BaseModel):
    """
    Base Transaction class. This class holds all the possible attributes of a transaction
    """

    transaction_id: Optional[str] = None
    portfolio_stock_id: Optional[str] = None
    transaction_type: Optional[TransactionType] = None
    transaction_date: Optional[str] = None
    transaction_price: Optional[str] = None
    quantity: Optional[str] = None
    order_type: Optional[OrderType] = None
    limit_price: Optional[str] = None
    transaction_value: Optional[str] = None
    realized_profit_loss: Optional[str] = None


class TransactionResponseBase(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None


class GetTransactionResponse(TransactionResponseBase):
    details: Optional[Any] = None

    class Config:
        orm_mode = True
        message = "Successfully fetched the transaction details!"
        schema_extra = {
            "example": {
                "status": True,
                "message": "Transaction found!",
                "details": {
                    "transaction_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "portfolio_stock_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "transaction_type": "buy",
                    "transaction_date": "2023-01-01",
                    "transaction_price": "23.5",
                    "quantity": "10",
                    "order_type": "market",
                    "limit_price": "",
                    "transaction_value": "235",
                    "realized_profit_loss": "20",
                },
            }
        }


class CreateTransaction(TransactionBase):
    """
    Transaction creation schema
    """

    portfolio_stock_id: str = Field(...)
    transaction_type: TransactionType = Field(...)
    transaction_date: datetime = Field(...)
    transaction_price: float = Field(...)
    quantity: int = Field(...)
    order_type: OrderType = Field(...)
    limit_price: Optional[float] = None
    transaction_value: float = Field(...)
    realized_profit_loss: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "portfolio_stock_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                "transaction_type": "buy",
                "transaction_date": "2023-01-01",
                "transaction_price": "23.5",
                "quantity": "10",
                "order_type": "market",
                "limit_price": "",
                "transaction_value": "235",
                "realized_profit_loss": "20",
            }
        }


class CreateTransactionResponse(TransactionResponseBase):
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully created the transaction!",
                "details": {
                    "portfolio_stock_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "transaction_type": "buy",
                    "transaction_date": "2023-01-01",
                    "transaction_price": "23.5",
                    "quantity": "10",
                    "order_type": "market",
                    "limit_price": "",
                    "transaction_value": "235",
                    "realized_profit_loss": "20",
                },
            }
        }


class UpdateTransaction(TransactionBase):
    """
    Transaction update schema. Properties to receive via API on update
    """

    transaction_id: str = Field(...)
    portfolio_stock_id: Optional[str] = None
    transaction_type: Optional[TransactionType] = None
    transaction_date: Optional[str] = None
    transaction_price: Optional[str] = None
    quantity: Optional[str] = None
    order_type: Optional[OrderType] = None
    limit_price: Optional[str] = None
    transaction_value: Optional[str] = None
    realized_profit_loss: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "transaction_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                "portfolio_stock_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                "transaction_type": "buy",
                "transaction_date": "2023-01-01",
                "transaction_price": "23.5",
                "quantity": "10",
                "order_type": "market",
                "limit_price": "",
                "transaction_value": "235",
                "realized_profit_loss": "20",
            }
        }


class UpdateTransactionResponse(TransactionResponseBase):
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully updated the transaction!",
                "details": {
                    "transaction_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "portfolio_stock_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "transaction_type": "buy",
                    "transaction_date": "2023-01-01",
                    "transaction_price": "23.5",
                    "quantity": "10",
                    "order_type": "market",
                    "limit_price": "",
                    "transaction_value": "235",
                    "realized_profit_loss": "20",
                },
            }
        }


class DeleteTransaction(TransactionBase):
    """
    Transaction delete schema. Properties to receive via API on delete
    """

    transaction_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "transaction_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
            }
        }


class DeleteTransactionResponse(TransactionResponseBase):
    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully deleted the transaction!",
            }
        }
