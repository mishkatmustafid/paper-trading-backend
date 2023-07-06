"""
Portfolio Stock module. This module contains handlers related
to portfolio stock create, read, update and delete.
"""

from typing import Any, Optional
from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from loguru import logger

from app import crud
from app.db.session import db_connection
from app.schemas import (
    CreatePortfolioStock,
    CreatePortfolioStockResponse,
    GetPortfolioStockResponse,
    UpdatePortfolioStock,
    UpdatePortfolioStockResponse,
    DeletePortfolioStock,
    DeletePortfolioStockResponse,
)
from app.utils.exceptions import InvalidUUIDError
from app.utils.uuid_validation import is_valid_uuid
from app.auth.bearer import JWTBearer
from app.utils.general import General
from app.utils.handle_error import handle_error

router = APIRouter()


@router.post(
    "/{portfolio_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=CreatePortfolioStockResponse,
    response_model_exclude_unset=True,
)
async def create_portfolio_stock(
    portfolio_id: str,
    payload: CreatePortfolioStock,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Creates a new portfolio stock based on the given user details via payload.
    """

    try:
        if not is_valid_uuid(portfolio_id):
            raise InvalidUUIDError(
                "Invalid UUID format for portfolio uuid",
                status_code=400,
            )
        if not is_valid_uuid(payload.asset_id):
            raise InvalidUUIDError(
                "Invalid UUID format for asset uuid",
                status_code=400,
            )
        if not crud.portfolio_stock.get_by_portfolio_id(db, portfolio_id):
            raise InvalidUUIDError(
                "Invalid portfolio uuid",
                status_code=400,
            )
        payload.portfolio_id = portfolio_id
        portfolio_stock = General.exclude_metadata(
            jsonable_encoder(crud.portfolio_stock.create(db, payload))
        )

        return {
            "status": True,
            "message": "Successfully created the Portfolio Stock!",
            "details": {
                "portfolio_stock_id": portfolio_stock["portfolio_stock_id"],
                "portfolio_id": portfolio_id,
                "name": portfolio_stock["name"],
                "asset_id": portfolio_stock["asset_id"],
                "quantity": portfolio_stock["quantity"],
                "purchase_date": portfolio_stock["purchase_date"],
                "purchase_price": portfolio_stock["purchase_price"],
                "average_purchase_price": portfolio_stock["average_purchase_price"],
                "total_quantity": portfolio_stock["total_quantity"],
                "total_investment": portfolio_stock["total_investment"],
            },
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.get(
    "/{portfolio_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=GetPortfolioStockResponse,
    response_model_exclude_unset=True,
)
async def get_portfolio_stock(
    portfolio_id: str,
    response: Response,
    portfolio_stock_id: Optional[str] = None,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Gets portfolio stock details.
    """

    try:
        if not is_valid_uuid(portfolio_id):
            raise InvalidUUIDError(
                "Invalid UUID format for portfolio uuid",
                status_code=400,
            )
        if portfolio_stock_id:
            if not is_valid_uuid(portfolio_stock_id):
                raise InvalidUUIDError(
                    "Invalid UUID format for portfolio stock uuid",
                    status_code=400,
                )
            if portfolio_stock := General.exclude_metadata(
                jsonable_encoder(
                    crud.portfolio_stock.get_by_portfolio_stock_id(
                        db, portfolio_stock_id
                    )
                )
            ):
                return {
                    "status": True,
                    "message": "Portfolio Stock Found!",
                    "details": {
                        "portfolio_stock_id": portfolio_stock["portfolio_stock_id"],
                        "portfolio_id": portfolio_id,
                        "name": portfolio_stock["name"],
                        "asset_id": portfolio_stock["asset_id"],
                        "quantity": portfolio_stock["quantity"],
                        "purchase_date": portfolio_stock["purchase_date"],
                        "purchase_price": portfolio_stock["purchase_price"],
                        "average_purchase_price": portfolio_stock[
                            "average_purchase_price"
                        ],
                        "total_quantity": portfolio_stock["total_quantity"],
                        "total_investment": portfolio_stock["total_investment"],
                    },
                }
            return {"status": False, "message": "Portfolio Stock Not Found!"}
        if portfolio_stocks := General.exclude_metadata(
            jsonable_encoder(crud.portfolio_stock.get_by_portfolio_id(db, portfolio_id))
        ):
            return {
                "status": True,
                "message": "All Portfolios Found!",
                "details": portfolio_stocks,
            }
        return {
            "status": False,
            "message": "Portfolio Stock Not Found!",
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.put(
    "/{portfolio_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=UpdatePortfolioStockResponse,
    response_model_exclude_unset=True,
)
async def update_portfolio_stock(
    portfolio_id: str,
    payload: UpdatePortfolioStock,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Updates a portfolio stock details
    """

    try:
        if not is_valid_uuid(portfolio_id):
            raise InvalidUUIDError(
                "Invalid UUID format for portfolio uuid",
                status_code=400,
            )
        if not is_valid_uuid(payload.portfolio_stock_id):
            raise InvalidUUIDError(
                "Invalid UUID format for portfolio stock uuid",
                status_code=400,
            )
        payload.portfolio_id = portfolio_id
        portfolio_stock = General.exclude_metadata(
            jsonable_encoder(
                crud.portfolio_stock.update(db, payload.portfolio_stock_id, payload)
            )
        )
        if portfolio_stock:
            details = payload.dict(exclude_unset=True)
            details["portfolio_stock_id"] = payload.portfolio_stock_id
            return {
                "status": True,
                "message": "Successfully updated the portfolio stock details!",
                "details": details,
            }

        return {
            "status": False,
            "message": "Portfolio Stock Not Found!",
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.delete(
    "/{portfolio_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=DeletePortfolioStockResponse,
    response_model_exclude_unset=True,
)
async def delete_portfolio_stock(
    portfolio_id: str,
    payload: DeletePortfolioStock,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Deletes a portfolio stock details.
    """

    try:
        if not is_valid_uuid(portfolio_id):
            raise InvalidUUIDError(
                "Invalid UUID format for portfolio uuid",
                status_code=400,
            )
        if not is_valid_uuid(payload.portfolio_stock_id):
            raise InvalidUUIDError(
                "Invalid UUID format for portfolio stock uuid",
                status_code=400,
            )
        portfolio_stock = crud.portfolio_stock.get_by_portfolio_stock_id(
            db, payload.portfolio_stock_id
        )
        if portfolio_stock:
            if portfolio_stock := crud.portfolio_stock.delete(
                db, payload.portfolio_stock_id
            ):
                return {
                    "status": True,
                    "message": "Successfully deleted the portfolio stock!",
                }

        return {
            "status": False,
            "message": "Portfolio Stock Not Found!",
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)
