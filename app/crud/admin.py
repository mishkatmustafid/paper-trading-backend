"""
Admin User CRUD module.
Provides functionality to read, create, update and delete of the admin user model.
"""

from pydantic import BaseModel


class CRUDAdminUser(BaseModel):
    """
    Admin user's CRUD operation's class.
    """

    # @staticmethod
    # def create(
    #     db: Session,
    #     payload_in: CreateAdminUser,
    # ):
    #     """
    #     Creates new admin user in the db.
    #     """
