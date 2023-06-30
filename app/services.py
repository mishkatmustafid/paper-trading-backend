"""Database initialisation and migration module"""

from typing import Optional

from alembic import command
from alembic.config import Config

from app.db.session import initialise


def run_migrations(script_location: str, db_url: Optional[str]) -> None:
    """
    Runs migrations
    """

    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(alembic_cfg, "head")


def init_db() -> None:
    """
    Initialises database engine.
    """
    initialise()
