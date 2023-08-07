"""
Transaction models module
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Identity, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

# from sqlalchemy.orm import relationship

from app.models import Base
from app.models.order_type import OrderType
from app.models.transaction_type import TransactionType
from app.models.transaction_status import TransactionStatus


class Transaction(Base):
    """
    Transaction class
    """

    __tablename__ = "transaction"

    id: int = Column(
        Integer,
        Identity(start=1, cycle=True),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )

    transaction_id: str = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    )

    portfolio_id: str = Column(
        UUID(as_uuid=True),
        ForeignKey("portfolio.portfolio_id"),
        nullable=False,
    )

    asset_id: str = Column(
        UUID(as_uuid=True),
        ForeignKey("assets.asset_id"),
        nullable=False,
    )

    transaction_type: enum = Column(Enum(TransactionType), nullable=False)
    transaction_status: enum = Column(Enum(TransactionStatus), nullable=False)
    transaction_date: datetime = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    transaction_price: float = Column(Float, nullable=False)
    quantity: int = Column(Integer, nullable=False)
    order_type: enum = Column(Enum(OrderType), nullable=False)
    limit_price: float = Column(Float, nullable=True)
    transaction_value = Column(Float, nullable=False)

    # Relationships
    # portfolio_stock = relationship("PortfolioStock", back_populates="transactions")

    @classmethod
    def get_by_transaction_id(cls, db: Session, transaction_id: str):
        """
        Gets transaction from database based on a given transaction id
        """

        return (
            db.query(Transaction)
            .where(Transaction.deleted_at == None)
            .filter(Transaction.transaction_id == transaction_id)
            .first()
        )

    @classmethod
    def get_by_portfolio_stock_id(cls, db: Session, portfolio_stock_id: str):
        """
        Gets all transaction from database based on a given portfolio stock id
        """

        return (
            db.query(Transaction)
            .where(Transaction.deleted_at == None)
            .filter(Transaction.portfolio_stock_id == portfolio_stock_id)
            .all()
        )

    @classmethod
    def get_by_asset_id(cls, db: Session, asset_id: str):
        """
        Gets all transaction from database based on a given asset id
        """

        return (
            db.query(Transaction)
            .where(Transaction.deleted_at == None)
            .filter(Transaction.asset_id == asset_id)
            .all()
        )
