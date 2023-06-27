"""
Database connection module
"""

from typing import Generator

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import settings

engine = create_engine(settings.DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def initialise() -> bool:  # pylint: disable=inconsistent-return-statements
    """
    Database connection initializer.
    """
    try:
        if engine.connect():
            return True

    except Exception as err:
        logger.error(f"DATABASE_CONNECTION_ERROR: {err}")
        raise err


def db_connection() -> Generator:
    """
    Database connection generator.
    Returns a generator object if engine connects successfully.
    """
    try:
        if initialise():
            db = SessionLocal()
            yield db
    finally:
        db.close()
