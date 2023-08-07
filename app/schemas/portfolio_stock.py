"""
Transaction schema module
"""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class PortfolioStockBase(BaseModel):
    """
    Base Portfolio Stock class. This class holds all the possible attributes of a portfolio stock
    """

    portfolio_stock_id: Optional[str] = None
    portfolio_id: Optional[str] = None
    asset_id: Optional[str] = None
    asset_name: Optional[str] = None
    quantity: Optional[int] = None
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = None
    total_investment: Optional[float] = None


class PortfolioStockResponseBase(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None


class GetPortfolioStockResponse(PortfolioStockResponseBase):
    details: Optional[Any] = None

    class Config:
        orm_mode = True
        message = "Successfully fetched the portfolio stock details!"
        schema_extra = {
            "example": {
                "status": True,
                "message": "Portfolio stock found!",
                "details": {
                    "portfolio_stock_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "asset_name": "Apple Inc.",
                    "quantity": 10,
                    "purchase_date": "2023-07-12T15:30:00",
                    "purchase_price": 2.3,
                    "total_investment": 230.0,
                },
            }
        }


class CreatePortfolioStock(PortfolioStockBase):
    """
    Portfolio creation schema
    """

    asset_id: str = Field(...)
    asset_name: str = Field(...)
    quantity: int = Field(...)
    purchase_date: datetime = Field(...)
    purchase_price: float = Field(...)
    total_investment: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                "asset_name": "Apple Inc.",
                "quantity": 10,
                "purchase_date": "2023-07-12T15:30:00",
                "purchase_price": 2.3,
                "total_investment": 230.0,
            }
        }


class CreatePortfolioStockResponse(PortfolioStockResponseBase):
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully created the portfolio!",
                "details": {
                    "portfolio_stock_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "asset_name": "Apple Inc.",
                    "quantity": 10,
                    "purchase_date": "2023-07-12T15:30:00",
                    "purchase_price": 2.3,
                    "total_investment": 230.0,
                },
            }
        }


class UpdatePortfolioStock(PortfolioStockBase):
    """
    PortfolioStock update schema. Properties to receive via API on update
    """

    portfolio_stock_id: Optional[str] = None
    portfolio_id: Optional[str] = None
    asset_id: Optional[str] = None
    quantity: Optional[int] = None
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = None
    total_investment: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                "asset_name": "Apple Inc.",
                "quantity": 10,
                "purchase_date": "2023-07-12T15:30:00",
                "purchase_price": 2.3,
                "total_investment": 230.0,
            }
        }


class UpdatePortfolioStockResponse(PortfolioStockResponseBase):
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully updated the portfolio stock!",
                "details": {
                    "portfolio_stock_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "asset_name": "Apple Inc.",
                    "quantity": 10,
                    "purchase_date": "2023-07-12T15:30:00",
                    "purchase_price": 2.3,
                    "total_investment": 230.0,
                },
            }
        }


class DeletePortfolioStockResponse(PortfolioStockResponseBase):
    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully deleted the portfolio stock!",
            }
        }
