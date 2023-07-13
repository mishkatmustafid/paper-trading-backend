"""
Market Data Historical models module
"""
import enum
import uuid

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
    def get_market_data_historical_by_market_data_historical_id(
        cls, db: Session, market_data_historical_id: str
    ):
        return (
            db.query(MarketDataHistorical)
            .where(MarketDataHistorical.deleted_at == None)
            .filter(
                MarketDataHistorical.market_data_historical_id
                == market_data_historical_id
            )
            .first()
        )

    @classmethod
    def get_market_data_historical_by_symbol(
        cls, db: Session, symbol: str, asset_type: AssetType
    ):
        """
        Gets all historical market data from database based on given symbol and asset type.
        """

        return (
            db.query(MarketDataHistorical)
            .where(MarketDataHistorical.deleted_at == None)
            .filter(MarketDataHistorical.symbol == symbol)
            .filter(MarketDataHistorical.asset_type == asset_type)
            .first()
        )

    @classmethod
    def get_market_data_historical_by_name(
        cls, db: Session, name: str, asset_type: AssetType
    ):
        """
        Gets all historical market data from database based on given name and asset type.
        """

        return (
            db.query(MarketDataHistorical)
            .where(MarketDataHistorical.deleted_at == None)
            .filter(MarketDataHistorical.name == name)
            .filter(MarketDataHistorical.asset_type == asset_type)
            .first()
        )
