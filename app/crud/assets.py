"""
Assets CRUD operations
"""

from datetime import datetime
from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models import Assets, Exchange
from app.schemas.assets import CreateAsset


class CRUDAssets(BaseModel):
    """
    class for Asset's CRUD operations.
    """

    @staticmethod
    def create(db: Session, payload_in: CreateAsset):
        serialized_data = jsonable_encoder(payload_in)
        db_obj = Assets(**serialized_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    @staticmethod
    def get_by_asset_id(db: Session, asset_id: str):
        return Assets.get_by_asset_id(db, asset_id)

    @staticmethod
    def get_by_name(db: Session, name: str, exchange: Exchange):
        return Assets.get_by_name(db, name, exchange)

    @staticmethod
    def get_by_symbol(db: Session, symbol: str, exchange: Exchange):
        return Assets.get_by_symbol(db, symbol, exchange)

    @staticmethod
    def get_multi(db: Session):
        return db.query(Assets).where(Assets.deleted_at == None).all()

    @staticmethod
    def update(
        db: Session,
        asset_id: str,
        obj_in: Union[Assets, Dict[str, Any]],
    ):
        """
        Updates attibutes of the given asset
        """
        if asset_details := Assets.get_by_asset_id(db, asset_id):
            obj_data = jsonable_encoder(asset_details)

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
                    setattr(asset_details, field, update_data[field])

            db.add(asset_details)
            db.commit()
            db.refresh(asset_details)

    def delete(self, db: Session, asset_id: str):
        # Delete performs a soft delete i.e. deleted_at attribute
        # is updated with a timestamp
        # Data would still be in the database but won't show up in
        # query result
        payload = {"deleted_at": datetime.utcnow()}

        return self.update(db, asset_id, payload)


assets = CRUDAssets()
