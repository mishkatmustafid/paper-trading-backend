"""
MarketDataHistorical CRUD operations
"""

from pydantic import BaseModel
from sqlalchemy.orm import Session


class CRUDMarketDataHistorical(BaseModel):
    """
    class for MarketDataHistorical's CRUD operations.
    """

    @staticmethod
    def get_price_by_symbol(db: Session, symbol: str):
        return {"symbol": symbol, "price": 234.56}


market_data_historical = CRUDMarketDataHistorical()
