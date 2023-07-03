"""
Portfolio Stock models module
"""

import enum
import uuid

from sqlalchemy import Column, Enum, ForeignKey, Identity, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, relationship

from app.models import Base
from app.models.asset_type import AssetType


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

    asset_id: str = Column(UUID(as_uuid=True), nullable=False)
    asset_type: enum = Column(Enum(AssetType), nullable=False)
    quantity: int = Column(Integer, nullable=False)
    purchase_date: str = Column(String, nullable=False)
    purchase_price: Numeric = Column(Numeric(10, 2), nullable=False)
    average_purchase_price: Numeric = Column(Numeric(10, 2), nullable=False)
    total_quantity: int = Column(Integer, nullable=False)
    total_investment: Numeric = Column(Numeric(10, 2), nullable=False)

    # Relationships
    # portfolio = relationship("Portfolio", back_populates="portfolio_stocks")

    @classmethod
    def get_portfolio_stock_by_id(cls, db: Session, primary_id: int):
        """
        Gets portfolio stock from database based on a given portfolio id.
        """

        return (
            db.query(PortfolioStock)
            .where(PortfolioStock.deleted_at == None)
            .filter(PortfolioStock.id == primary_id)
            .first()
        )

    @classmethod
    def get_portfolio_by_portfolio_id(cls, portfolio_id: int, db: Session):
        """
        Gets all portfolio from database based on a given user id.
        """

        return (
            db.query(PortfolioStock)
            .where(PortfolioStock.deleted_at == None)
            .filter(PortfolioStock.portfolio_id == portfolio_id)
            .all()
        )
