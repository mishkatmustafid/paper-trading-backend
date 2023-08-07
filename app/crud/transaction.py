"""
Transaction CRUD operations
"""

from datetime import datetime
from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models import Transaction
from app.schemas.transaction import CreateTransaction, UpdateTransaction


class CRUDTransaction(BaseModel):
    """
    class for Transaction's CRUD operations.
    """

    @staticmethod
    def create(db: Session, payload_in: CreateTransaction):
        serialized_data = jsonable_encoder(payload_in)
        db_obj = Transaction(**serialized_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    @staticmethod
    def get_by_transaction_id(db: Session, transaction_id: str):
        return Transaction.get_by_transaction_id(db, transaction_id)

    @staticmethod
    def get_by_portfolio_id(db: Session, portfolio_id: str):
        return Transaction.get_by_portfolio_id(db, portfolio_id)

    @staticmethod
    def get_by_asset_id(db: Session, asset_id: str):
        return Transaction.get_by_asset_id(db, asset_id)

    @staticmethod
    def update(
        db: Session,
        transaction_id: str,
        obj_in: Union[UpdateTransaction, Dict[str, Any]],
    ):
        """
        Updates attibutes of the given transaction
        """

        # retrieve details of the given transaction
        if transaction_details := Transaction.get_by_transaction_id(db, transaction_id):
            obj_data = jsonable_encoder(transaction_details)

            # check if the given payload (i.e. obj_in) is in a
            # dictionary instance
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                # only payload is set to be updated
                update_data = obj_in.dict(exclude_unset=True)

            # update only those attributes sent via payload
            for field in update_data:
                if field in obj_data:
                    setattr(transaction_details, field, update_data[field])

            db.add(transaction_details)
            db.commit()
            db.refresh(transaction_details)
        return transaction_details

    def delete(self, db: Session, transaction_id: str):
        # Delete performs a soft delete i.e. deleted_at attribute
        # is updated with a timestamp
        # Data would still be in the database but won't show up in
        # query result
        payload = {"deleted_at": datetime.utcnow()}

        return self.update(db, transaction_id, payload)


transaction = CRUDTransaction()
