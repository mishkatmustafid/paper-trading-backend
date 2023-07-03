"""
Transaction models module
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Identity, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.order_type import OrderType
from app.models.transaction_type import TransactionType


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

    portfolio_stock_id: str = Column(
        UUID(as_uuid=True),
        ForeignKey("portfolio.portfolio_id"),
        nullable=False,
    )

    transaction_type: enum = Column(Enum(TransactionType), nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    transaction_price: float = Column(Float, nullable=False)
    quantity: int = Column(Integer, nullable=False)
    order_type: enum = Column(Enum(OrderType), nullable=False)
    limit_price: float = Column(Float, nullable=True)
    transaction_value = Column(Float, nullable=False)
    realized_profit_loss = Column(Float, nullable=False)

    # Relationships
    # portfolio_stock = relationship("PortfolioStock", back_populates="transactions")
