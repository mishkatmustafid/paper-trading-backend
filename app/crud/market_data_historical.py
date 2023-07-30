"""
MarketDataHistorical CRUD operations
"""

from datetime import datetime
from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models import MarketDataHistorical
from app.schemas.market_data_historical import CreateMarketDataHistorical


class CRUDMarketDataHistorical(BaseModel):
    """
    class for MarketDataHistorical's CRUD operations.
    """

    @staticmethod
    def create(db: Session, payload_in: CreateMarketDataHistorical):
        serialized_data = jsonable_encoder(payload_in)
        db_obj = MarketDataHistorical(**serialized_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    @staticmethod
    def get_by_market_data_historical_id(db: Session, market_data_historical_id: str):
        return MarketDataHistorical.get_market_data_historical_by_market_data_historical_id(
            db, market_data_historical_id
        )

    @staticmethod
    def get_by_asset_id(db: Session, asset_id: str):
        return MarketDataHistorical.get_by_asset_id(db, asset_id)

    @staticmethod
    def update(
        db: Session,
        market_data_historical_id: str,
        obj_in: Union[MarketDataHistorical, Dict[str, Any]],
    ):
        """
        Updates attibutes of the given marketdata historical
        """

        # retrieve details of the given portfolio
        if market_data_historical_details := MarketDataHistorical.get_by_market_data_historical_id(
            db, market_data_historical_id
        ):
            obj_data = jsonable_encoder(market_data_historical_details)

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
                    setattr(market_data_historical_details, field, update_data[field])

            db.add(market_data_historical_details)
            db.commit()
            db.refresh(market_data_historical_details)
        return market_data_historical_details

    def delete(self, db: Session, market_data_historical_id: str):
        # Delete performs a soft delete i.e. deleted_at attribute
        # is updated with a timestamp
        # Data would still be in the database but won't show up in
        # query result
        payload = {"deleted_at": datetime.utcnow()}

        return self.update(db, market_data_historical_id, payload)


market_data_historical = CRUDMarketDataHistorical()
