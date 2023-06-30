"""
User CRUD module.
Provides functionality to read, create, update, and delete
functionalities of the user model
"""

from datetime import datetime
from typing import Any, Dict, List, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import auth
from app.models.user import User
from app.schemas.user import CreateUser, UpdateUser


class CRUDUser(BaseModel):
    """
    class for user's CRUD operations.
    """

    # pylint: disable=singleton-comparison

    @staticmethod
    def create(db: Session, payload_in: CreateUser):
        payload_in["password"] = auth.hash_password(payload_in["password"])
        db_object = User(**(jsonable_encoder(payload_in)))
        db.add(db_object)
        db.commit()

        return db_object

    @staticmethod
    def get_by_id(db: Session, pid: int):
        return User.get_by_id(db, pid)

    @staticmethod
    def get_by_userid(db: Session, user_id: str):
        return User.get_by_userid(db, user_id)

    @staticmethod
    def get_by_email(db: Session, email: str):
        return User.get_by_email(db, email)

    @staticmethod
    def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return (
            db.query(User)
            .where(User.deleted_at == None)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self, db: Session, user_id: str, obj_in: Union[UpdateUser, Dict[str, Any]]
    ):
        """
        Updates attributes of the given user
        """

        # retrieve details of the given user id and
        user_details = self.get_by_userid(db, user_id)

        if user_details:
            obj_data = jsonable_encoder(user_details)

            # check if the given payload (i.e. obj_in) is an
            # dictionary instance.
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                # only payload is set to be updated.
                update_data = obj_in.dict(exclude_unset=True)

            # update only those attributes sent via payload
            for field in obj_data:
                if field in update_data:
                    setattr(user_details, field, update_data[field])

            db.add(user_details)
            db.commit()
            db.refresh(user_details)
        return user_details

    def delete(self, db: Session, user_id: str):
        # Delete performs a soft delete i.e. deleted_at attribute
        # is updated with a timestamp.
        # Data would still be in the database but won't show up in
        # query result
        payload = {"deleted_at": datetime.utcnow()}

        return self.update(db, user_id, payload)


user = CRUDUser()
