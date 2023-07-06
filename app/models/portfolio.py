"""
Portfolio models module
"""

import uuid

from sqlalchemy import Column, ForeignKey, Identity, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models import Base


class Portfolio(Base):
    """Portfolio class"""

    __tablename__ = "portfolio"

    id: int = Column(
        Integer,
        Identity(start=1, cycle=True),
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )
    portfolio_id: str = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    )
    user_id: str = Column(
        UUID(as_uuid=True),
        ForeignKey("user.user_id"),
        nullable=False,
    )
    name: str = Column(String(50), nullable=False)

    @classmethod
    def get_by_portfolio_id(cls, db: Session, portfolio_id: str):
        """
        Gets portfolio from database based on a given portfolio id.
        """

        return (
            db.query(Portfolio)
            .where(Portfolio.deleted_at == None)
            .filter(Portfolio.portfolio_id == portfolio_id)
            .first()
        )

    @classmethod
    def get_portfolio_by_user_id(cls, db: Session, user_id: int):
        """
        Gets all portfolio from database based on a given user id.
        """

        return (
            db.query(Portfolio)
            .where(Portfolio.deleted_at == None)
            .filter(Portfolio.user_id == user_id)
            .all()
        )
