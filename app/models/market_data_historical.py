"""
Market Data Historical models module
"""
import uuid
import enum

from sqlalchemy import Column, Date, Enum, Float, Identity, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models import Base
from app.models.asset_type import AssetType


class MarketDataHistorical(Base):
    """
    MarketDataHistorical class
    """

    __tablename__ = "market_data_historical"

    id: int = Column(
        Integer,
        Identity(start=1, cycle=True),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )
    market_data_historical_id: str = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    )
    date = Column(Date, nullable=False)
    name: str = Column(String(50), nullable=False)
    asset_type: enum = Column(Enum(AssetType), nullable=False)
    symbol: str = Column(String(50), nullable=False, index=True)
    open: float = Column(Float, nullable=False)
    high: float = Column(Float, nullable=False)
    low: float = Column(Float, nullable=False)
    close: float = Column(Float, nullable=False)
    volume: int = Column(Integer, nullable=False)

    @classmethod
    def get_market_data_historical_by_symbol(cls, symbol: str, db: Session):
        """
        Gets all historical market data from database based on given symbol.
        """

        return (
            db.query(MarketDataHistorical)
            .where(MarketDataHistorical.deleted_at == None)
            .filter(MarketDataHistorical.symbol == symbol)
            .all()
        )
