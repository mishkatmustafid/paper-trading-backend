"""
MarketDataHistorical CRUD operations
"""

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models import MarketDataHistorical, asset_type


class CRUDMarketDataHistorical(BaseModel):
    """
    class for MarketDataHistorical's CRUD operations.
    """

    @staticmethod
    def get_price_by_symbol(db: Session, symbol: str, asset_type: asset_type):
        details = MarketDataHistorical.get_market_data_historical_by_symbol(
            db, symbol, asset_type
        )
        open = details["open"]
        high = details["high"]
        low = details["low"]
        close = details["close"]
        price = (open + high + low + close) / 4.0
        return price


market_data_historical = CRUDMarketDataHistorical()
