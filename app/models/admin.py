"""
User models module
"""
import enum
import uuid

from sqlalchemy import Boolean, Column, Enum, Identity, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models.admin_level import AdminLevel
from app.models.base import Base


class AdminUser(Base):
    """
    Admin User class
    """

    __tablename__ = "admin_user"

    id: int = Column(
        Integer,
        Identity(start=1, cycle=True),
        autoincrement=True,
        nullable=False,
        unique=True,
        index=True,
    )
    user_id: str = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    )
    full_name: str = Column(String(50), nullable=False)
    email: str = Column(String(100), nullable=False, unique=True, index=True)
    username: str = Column(String(50), nullable=False, unique=True, index=True)
    password: str = Column(String(100), nullable=False)
    admin_level: enum = Column(Enum(AdminLevel), nullable=False)
    is_active: bool = Column(Boolean, default=True)

    # pylint: disable=singleton-comparison

    @classmethod
    def get_by_id(cls, db: Session, primary_id: int):
        """
        Gets admin user from database based on the given id.
        """

        return (
            db.query(AdminUser)
            .where(AdminUser.deleted_at == None)
            .filter(AdminUser.id == primary_id)
            .first()
        )

    @classmethod
    def get_by_user_id(cls, db: Session, user_id: str):
        """
        Gets admin user from database based on the given user id.
        """

        return (
            db.query(AdminUser)
            .where(AdminUser.deleted_at == None)
            .filter(AdminUser.user_id == user_id)
            .first()
        )

    @classmethod
    def get_by_email(cls, db: Session, email: str):
        """
        Gets admin user from database based on the given email.
        """
        return (
            db.query(AdminUser)
            .where(AdminUser.deleted_at == None)
            .filter(AdminUser.email == email)
            .first()
        )

    @classmethod
    def get_by_username(cls, db: Session, username: str):
        """
        Gets admin user from database based on the given username.
        """
        return (
            db.query(AdminUser)
            .where(AdminUser.deleted_at == None)
            .filter(AdminUser.username == username)
            .first()
        )
