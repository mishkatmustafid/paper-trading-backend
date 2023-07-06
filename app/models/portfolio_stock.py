"""
Portfolio Stock models module
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Identity, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, relationship

from app.models import Base


class PortfolioStock(Base):
    """
    PortfolioStock class
    """

    __tablename__ = "portfolio_stock"

    id: int = Column(
        Integer,
        Identity(start=1, cycle=True),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )
    portfolio_stock_id: str = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    )

    portfolio_id: str = Column(
        UUID(as_uuid=True), ForeignKey("portfolio.portfolio_id"), nullable=False
    )

    asset_id: str = Column(
        UUID(as_uuid=True),
        ForeignKey("market_data_historical.market_data_historical_id"),
        nullable=False,
    )
    quantity: int = Column(Integer, nullable=False)
    purchase_date: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    purchase_price: Numeric = Column(Numeric(10, 2), nullable=False)
    average_purchase_price: Numeric = Column(Numeric(10, 2), nullable=False)
    total_quantity: int = Column(Integer, nullable=False)
    total_investment: Numeric = Column(Numeric(10, 2), nullable=False)

    # Relationships
    # portfolio = relationship("Portfolio", back_populates="portfolio_stocks")

    @classmethod
    def get_by_portfolio_stock_id(cls, db: Session, portfolio_stock_id: int):
        """
        Gets portfolio stock from database based on a given portfolio id.
        """

        return (
            db.query(PortfolioStock)
            .where(PortfolioStock.deleted_at == None)
            .filter(PortfolioStock.portfolio_stock_id == portfolio_stock_id)
            .first()
        )

    @classmethod
    def get_by_portfolio_id(cls, db: Session, portfolio_id: int):
        """
        Gets all portfolio from database based on a given portfolio id.
        """

        return (
            db.query(PortfolioStock)
            .where(PortfolioStock.deleted_at == None)
            .filter(PortfolioStock.portfolio_id == portfolio_id)
            .all()
        )
