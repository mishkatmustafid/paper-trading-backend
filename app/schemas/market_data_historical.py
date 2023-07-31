"""
Market Data Historical schema module
"""

from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field


class MarketDataHistorical(BaseModel):
    market_data_historical_id: Optional[str] = None
    asset_id: Optional[str] = None
    datetime: Optional[dt] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None


class MarketDataHistoricalResponseBase(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None


class GetDataResponse(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully got the data!",
                "details": {
                    "market_data_historical_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "datetime": "2023-07-12T15:30:00",
                    "open": 30000,
                    "high": 30000,
                    "low": 30000,
                    "close": 30000,
                    "volume": 30000,
                },
            }
        }


class GetAllDataResponse(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None
    details: Optional[list] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully got all the data!",
                "details": [
                    {
                        "market_data_historical_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                        "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                        "datetime": "2023-07-12T15:30:00",
                        "open": 30000,
                        "high": 30000,
                        "low": 30000,
                        "close": 30000,
                        "volume": 30000,
                    }
                ],
            }
        }


class CreateMarketDataHistorical(MarketDataHistorical):
    asset_id: str = Field(...)
    datetime: dt = Field(...)
    open: float = Field(...)
    high: float = Field(...)
    low: float = Field(...)
    close: float = Field(...)
    volume: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                "datetime": "2023-07-12T15:30:00",
                "open": 30000,
                "high": 30000,
                "low": 30000,
                "close": 30000,
                "volume": 30000,
            }
        }


class CreateMarketDataHistoricalResponse(MarketDataHistoricalResponseBase):
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully created the market data historical",
                "details": {
                    "market_data_historical_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "asset_id": "8a648c97-faae-44ee-bb57-3ece478fe263",
                    "datetime": "2023-07-12T15:30:00",
                    "open": 30000,
                    "high": 30000,
                    "low": 30000,
                    "close": 30000,
                    "volume": 30000,
                },
            }
        }
