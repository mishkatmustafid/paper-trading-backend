"""
Assets models module
"""
import enum
import uuid

from sqlalchemy import Column, Enum, Float, Identity, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, relationship

from app.models import Base
from app.models.exchange import Exchange


class Assets(Base):
    """
    Assets class
    """

    __tablename__ = "assets"

    id: int = Column(
        Integer,
        Identity(start=1, cycle=True),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )
    asset_id: str = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    )
    symbol: str = Column(String(20), nullable=False)
    name: str = Column(String(20), nullable=False)
    exchange: enum = Column(Enum(Exchange), nullable=False)
    current_price: float = Column(Float, nullable=False)
    previous_close_price: float = Column(Float, nullable=False)
    open: float = Column(Float, nullable=False)
    high: float = Column(Float, nullable=False)
    low: float = Column(Float, nullable=False)
    close: float = Column(Float, nullable=False)
    volume: int = Column(Integer, nullable=False)
    market_cap: float = Column(Float, nullable=False)

    # Relationships
    market_data_historical = relationship(
        "MarketDataHistorical", back_populates="assets"
    )

    @classmethod
    def get_asset_by_asset_id(cls, db: Session, asset_id: str):
        return (
            db.query(Assets)
            .where(Assets.deleted_at == None)
            .filter(Assets.asset_id == asset_id)
            .first()
        )

    @classmethod
    def get_asset_by_symbol(cls, db: Session, symbol: str, exchange: Exchange):
        """
        Gets all historical market data from database based on given symbol and asset type.
        """

        return (
            db.query(Assets)
            .where(Assets.deleted_at == None)
            .filter(Assets.symbol == symbol)
            .filter(Assets.exchange == exchange)
            .first()
        )

    @classmethod
    def get_asset_by_name(cls, db: Session, name: str, exchange: Exchange):
        """
        Gets all historical market data from database based on given name and asset type.
        """

        return (
            db.query(Assets)
            .where(Assets.deleted_at == None)
            .filter(Assets.name == name)
            .filter(Assets.exchange == exchange)
            .first()
        )
