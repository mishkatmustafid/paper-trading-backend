"""
User models module
"""

import uuid

from sqlalchemy import Boolean, Column, Enum, Identity, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models import Base
from app.models.profile_status import ProfileStatus


class User(Base):
    """User class"""

    __tablename__ = "user"

    # required for signup
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
    email: str = Column(String(100), unique=True, nullable=False, index=True)
    password: str = Column(String(100), nullable=False)
    is_active: bool = Column(Boolean, default=True)
    profile_status = Column(Enum(ProfileStatus), nullable=True)

    @classmethod
    def get_by_user_id(cls, db: Session, user_id: str):
        """
        Gets user from database based on the given user id.
        """

        return (
            db.query(User)
            .where(User.deleted_at == None)
            .filter(User.user_id == user_id)
            .first()
        )

    @classmethod
    def get_by_email(cls, db: Session, email: str):
        """
        Gets user from database based on the given email.
        """
        return (
            db.query(User)
            .where(User.deleted_at == None)
            .filter(User.email == email)
            .first()
        )
