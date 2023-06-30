"""
Base module for all the models
"""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base, declared_attr

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    """
    Base class
    """

    __abstract__ = True

    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)

    @classmethod
    def get_searchable_fields(cls, key=None):
        """Converts searchable_fields into objects"""

    @classmethod
    def get_filterable_fields(cls, key=None):
        """Converts filterable_fields into objects"""
