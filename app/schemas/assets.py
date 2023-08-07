"""
Assets schema module
"""

from typing import Optional, Any

from pydantic import BaseModel, Field

from app.models import Exchange


class AssetsBase(BaseModel):
    asset_id: Optional[str] = None
    symbol: Optional[str] = None
    name: Optional[str] = None
    exchange: Optional[Exchange] = None
    current_price: Optional[float] = None
    previous_close_price: Optional[float] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[int] = None
    market_cap: Optional[float] = None


class AssetsResponseBase(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None


class GetPriceResponse(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None
    details: Optional[Any] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully got the data!",
                "details": {
                    "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "symbol": "APPL",
                    "name": "Apple Inc.",
                    "exchange": "nyse",
                    "current_price": 30000,
                    "previous_close_price": 30000,
                    "open": 30000,
                    "high": 30000,
                    "low": 30000,
                    "volume": 30000,
                    "market_cap": 30000,
                },
            }
        }


class CreateAsset(AssetsBase):
    symbol: str = Field(...)
    name: str = Field(...)
    exchange: str = Field(...)
    current_price: float = Field(...)
    previous_close_price: float = Field(...)
    open: float = Field(...)
    high: float = Field(...)
    low: float = Field(...)
    volume: int = Field(...)
    market_cap: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "symbol": "APPL",
                "name": "Apple Inc.",
                "exchange": "NYSE",
                "current_price": 30000,
                "previous_close_price": 30000,
                "open": 30000,
                "high": 30000,
                "low": 30000,
                "volume": 30000,
                "market_cap": 30000,
            }
        }


class CreateAssetResponse(AssetsResponseBase):
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully created the market data historical",
                "details": {
                    "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "symbol": "APPL",
                    "name": "Apple Inc.",
                    "exchange": "nyse",
                    "current_price": 30000,
                    "previous_close_price": 30000,
                    "open": 30000,
                    "high": 30000,
                    "low": 30000,
                    "volume": 30000,
                    "market_cap": 30000,
                },
            }
        }


class DeleteAsset(AssetsBase):
    """
    Asset delete schema. Properties to receive via API on delete
    """

    transaction_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
            }
        }


class DeleteAssetResponse(AssetsBase):
    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully deleted the asset!",
            }
        }
