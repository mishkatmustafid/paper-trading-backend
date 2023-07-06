from typing import Optional

from pydantic import BaseModel, Field


class GetPriceResponse(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully got the price!",
                "details": {"symbol": "BTCUSDT", "price": "9000.0"},
            }
        }


class GetDetailsResponse(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully got the details!",
                "details": {
                    "symbol": "BTCUSDT",
                    "open": "9000.00",
                    "high": "9000.00",
                    "low": "9000.00",
                    "volume": "9000.00",
                },
            }
        }


class GetKlinesResponse(BaseModel):
    status: Optional[bool] = True
    message: Optional[str] = None
    details: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "message": "Successfully got the klines!",
                "details": {
                    "symbol": "BTCUSDT",
                    "interval": "1m",
                    "limit": "100",
                    "klines": [
                        {
                            "open_time": 1588954400,
                            "open": "9000.00",
                            "high": "9000.00",
                            "low": "9000.00",
                            "close": "9000.00",
                            "volume": "9000.00",
                            "close_time": 1588954400,
                            "quote_asset_volume": "9000.00",
                            "number_of_trades": 0,
                            "taker_buy_base_asset_volume": "9000.00",
                            "taker_buy_quote_asset_volume": "9000.00",
                            "ignore": "",
                        }
                    ],
                },
            }
        }
