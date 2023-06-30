"""
Seed module.
"""
from typing import Any

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth import auth
from app.core.config import settings
from app.models.admin import AdminUser

engine = create_engine(settings.DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()


def is_user_exists() -> Any:
    superuser = AdminUser.get_by_username(
        db,
        settings.SUPER_ADMIN_USER,
    )

    return bool(superuser)


def create_superuser() -> Any:
    db_object = AdminUser(
        full_name="Paper Trade Admin",
        email="hello@gmail.com",
        username=settings.SUPER_ADMIN_USER,
        password=auth.hash_password(settings.SUPER_ADMIN_PW),
        admin_level="admin",
        is_active=True,
    )
    db.add(db_object)
    db.commit()

    logger.info("Database is populated with the initial data")


if __name__ == "__main__":
    if is_user_exists():
        logger.info("Initial data is already populated. Nothing to do!")
    else:
        create_superuser()
