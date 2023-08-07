"""
Transaction schema module
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from app.models.order_type import OrderType
from app.models.transaction_status import TransactionStatus
from app.models.transaction_type import TransactionType


class TransactionBase(BaseModel):
    """
    Base Transaction class. This class holds all the possible attributes of a transaction
    """

    transaction_id: Optional[str] = None
    portfolio_id: Optional[str] = None
    asset_id: Optional[str] = None
    transaction_type: Optional[TransactionType] = None
    transaction_status: Optional[TransactionStatus] = None
    transaction_date: Optional[datetime] = None
    transaction_price: Optional[str] = None
    quantity: Optional[str] = None
    order_type: Optional[OrderType] = None
    limit_price: Optional[str] = None
    transaction_value: Optional[str] = None


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
                    "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "transaction_type": "buy",
                    "transaction_status": "pending",
                    "transaction_date": "2023-07-12T15:30:00",
                    "transaction_price": 23.5,
                    "quantity": 10,
                    "order_type": "market",
                    "limit_price": "",
                    "transaction_value": 235,
                },
            }
        }


class CreateTransaction(TransactionBase):
    """
    Transaction creation schema
    """

    portfolio_id: Optional[str] = None
    asset_id: str = Field(...)
    transaction_type: str = Field(...)
    transaction_status: str = Field(...)
    transaction_date: datetime = Field(...)
    transaction_price: float = Field(...)
    quantity: int = Field(...)
    order_type: str = Field(...)
    limit_price: Optional[float] = None
    transaction_value: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                "transaction_type": "BUY",
                "transaction_status": "PENDING",
                "transaction_date": "2023-07-12T15:30:00",
                "transaction_price": 23.5,
                "quantity": 10,
                "order_type": "MARKET",
                "limit_price": None,
                "transaction_value": 235,
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
                    "transaction_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "transaction_type": "buy",
                    "transaction_status": "pending",
                    "transaction_date": "2023-07-12T15:30:00",
                    "transaction_price": 23.5,
                    "quantity": 10,
                    "order_type": "market",
                    "limit_price": "",
                    "transaction_value": 235,
                },
            }
        }


class UpdateTransaction(TransactionBase):
    """
    Transaction update schema. Properties to receive via API on update
    """

    transaction_id: Optional[str] = None
    portfolio_id: Optional[str] = None
    asset_id: Optional[str] = None
    transaction_type: Optional[str] = None
    transaction_status: Optional[str] = None
    transaction_date: Optional[str] = None
    transaction_price: Optional[str] = None
    quantity: Optional[str] = None
    order_type: Optional[str] = None
    limit_price: Optional[str] = None
    transaction_value: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                "transaction_type": "BUY",
                "transaction_status": "PENDING",
                "transaction_date": "2023-07-12T15:30:00",
                "transaction_price": 23.5,
                "quantity": 10,
                "order_type": "MARKET",
                "limit_price": "",
                "transaction_value": 235,
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
                    "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "transaction_type": "buy",
                    "transaction_status": "pending",
                    "transaction_date": "2023-07-12T15:30:00",
                    "transaction_price": 23.5,
                    "quantity": 10,
                    "order_type": "market",
                    "limit_price": "",
                    "transaction_value": 235,
                },
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
