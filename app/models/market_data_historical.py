"""
Market Data Historical models module
"""
import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, Identity, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models import Base

# from sqlalchemy.orm import relationship


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
    asset_id: str = Column(
        UUID(as_uuid=True), ForeignKey("assets.asset_id"), nullable=False
    )
    datetime: datetime = Column(DateTime, nullable=False)
    open: float = Column(Float, nullable=False)
    high: float = Column(Float, nullable=False)
    low: float = Column(Float, nullable=False)
    close: float = Column(Float, nullable=False)
    volume: int = Column(Integer, nullable=False)

    # Relationships
    # asset = relationship(Assets, back_populates="market_data_historical")

    @classmethod
    def get_by_market_data_historical_id(
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
    def get_by_asset_id(cls, db: Session, asset_id: str):
        """
        Gets historical data based on given asset id
        """
        return (
            db.query(MarketDataHistorical)
            .where(MarketDataHistorical.deleted_at == None)
            .filter(MarketDataHistorical.asset_id == asset_id)
            .all()
        )
