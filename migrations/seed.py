"""
Seed module.
"""
from typing import Any

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth import auth
from app.core.config import settings

# from app.models.admin_user import AdminUser

engine = create_engine(settings.DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
