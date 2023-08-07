"""
Portfolio schema module
"""
from typing import Any, Optional

from pydantic import BaseModel, Field


class PortfolioBase(BaseModel):
    """
    Base Portfolio class. This class holds all the possible attributes of a portfolio
    """

    portfolio_id: Optional[str] = None
    user_id: Optional[str] = None
    name: Optional[str] = None


class PortfolioResponseBase(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None


class GetPortfolioResponse(PortfolioResponseBase):
    details: Optional[Any] = None

    class Config:
        orm_mode = True
        message = "Successfully fetched the portfolio details!"
        schema_extra = {
            "example": {
                "status": True,
                "message": "Portfolio found!",
                "details": {
                    "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "user_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "name": "John Doe",
                    "portfolio_stocks": [
                        {
                            "portfolio_stock_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                            "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                            "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                            "asset_name": "Apple Inc.",
                            "quantity": 10,
                            "purchase_date": "2023-07-12T15:30:00",
                            "purchase_price": 2.3,
                            "total_investment": 230.0,
                        }
                    ],
                },
            }
        }


class CreatePortfolio(PortfolioBase):
    """
    Portfolio creation schema
    """

    name: str = Field(...)

    class Config:
        schema_extra = {"example": {"name": "Practice 01"}}


class CreatePortfolioResponse(PortfolioResponseBase):
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully created the portfolio!",
                "details": {
                    "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "user_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "name": "Practice 01",
                },
            }
        }


class UpdatePortfolio(PortfolioBase):
    """
    Portfolio update schema. Properties to receive via API on update
    """

    portfolio_id: str = Field(...)
    name: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                "name": "Practice 01",
            }
        }


class UpdatePortfolioResponse(PortfolioResponseBase):
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully updated the portfolio!",
                "details": {
                    "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "user_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "name": "Practice 01",
                },
            }
        }


class DeletePortfolio(PortfolioBase):
    """
    Portfolio delete schema. Properties to receive via API on delete
    """

    portfolio_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "portfolio_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
            }
        }


class DeletePortfolioResponse(PortfolioResponseBase):
    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully deleted the portfolio!",
            }
        }
