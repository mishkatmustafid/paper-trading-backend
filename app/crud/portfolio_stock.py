"""
PortfolioStock CRUD operations
"""

from datetime import datetime
from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models import PortfolioStock
from app.schemas.portfolio_stock import CreatePortfolioStock, UpdatePortfolioStock


class CRUDPortfolioStock(BaseModel):
    """
    class for PortfolioStock's CRUD operations.
    """

    @staticmethod
    def create(db: Session, payload_in: CreatePortfolioStock):
        serialized_data = jsonable_encoder(payload_in)
        db_obj = PortfolioStock(**serialized_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    @staticmethod
    def get_by_portfolio_stock_id(db: Session, portfolio_stock_id: str):
        return PortfolioStock.get_by_portfolio_stock_id(db, portfolio_stock_id)

    @staticmethod
    def get_by_portfolio_id(db: Session, portfolio_id: str):
        return PortfolioStock.get_by_portfolio_id(db, portfolio_id)

    @staticmethod
    def update(
        db: Session,
        portfolio_stock_id: str,
        obj_in: Union[UpdatePortfolioStock, Dict[str, Any]],
    ):
        """
        Updates attibutes of the given portfolio stock
        """

        # retrieve details of the given portfolio
        if portfolio_stock_details := PortfolioStock.get_by_portfolio_stock_id(
            db, portfolio_stock_id
        ):
            obj_data = jsonable_encoder(portfolio_stock_details)

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
                    setattr(portfolio_stock_details, field, update_data[field])

            db.add(portfolio_stock_details)
            db.commit()
            db.refresh(portfolio_stock_details)

    def delete(self, db: Session, portfolio_stock_id: str):
        # Delete performs a soft delete i.e. deleted_at attribute
        # is updated with a timestamp
        # Data would still be in the database but won't show up in
        # query result
        payload = {"deleted_at": datetime.utcnow()}

        return self.update(db, portfolio_stock_id, payload)


portfolio_stock = CRUDPortfolioStock()
