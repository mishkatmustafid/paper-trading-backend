"""
Portfolio module. This module contains handlers related
to portfolio create, read, update and delete.
"""

from typing import Any, Optional
from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from loguru import logger

from app import crud
from app.db.session import db_connection
from app.schemas import (
    CreatePortfolio,
    CreatePortfolioResponse,
    GetPortfolioResponse,
    UpdatePortfolio,
    UpdatePortfolioResponse,
    DeletePortfolio,
    DeletePortfolioResponse,
)
from app.utils.exceptions import InvalidUUIDError
from app.utils.uuid_validation import is_valid_uuid
from app.auth.bearer import JWTBearer
from app.utils.general import General
from app.utils.handle_error import handle_error

router = APIRouter()


@router.post(
    "/{user_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=CreatePortfolioResponse,
    response_model_exclude_unset=True,
)
async def create_portfolio(
    user_id: str,
    payload: CreatePortfolio,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Creates a new portfolio based on the given user details via payload.
    """

    try:
        if not is_valid_uuid(user_id):
            raise InvalidUUIDError(
                "Invalid UUID format for user uuid",
                status_code=400,
            )
        if not crud.user.get_by_user_id(db, user_id):
            raise InvalidUUIDError(
                "Invalid user uuid",
                status_code=400,
            )
        payload.user_id = user_id
        portfolio = General.exclude_metadata(
            jsonable_encoder(crud.portfolio.create(db, payload))
        )

        return {
            "status": True,
            "message": "Successfully created the Portfolio!",
            "details": {
                "portfolio_id": portfolio["portfolio_id"],
                "user_id": user_id,
                "name": portfolio["name"],
            },
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.get(
    "/{user_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=GetPortfolioResponse,
    response_model_exclude_unset=True,
)
async def get_portfolio(
    user_id: str,
    response: Response,
    portfolio_id: Optional[str] = None,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Gets portfolio details.
    """

    try:
        if not is_valid_uuid(user_id):
            raise InvalidUUIDError(
                "Invalid UUID format for user uuid",
                status_code=400,
            )
        if portfolio_id:
            if not is_valid_uuid(portfolio_id):
                raise InvalidUUIDError(
                    "Invalid UUID format for portfolio uuid",
                    status_code=400,
                )
            if portfolio := General.exclude_metadata(
                jsonable_encoder(crud.portfolio.get_by_portfolio_id(db, portfolio_id))
            ):
                return {
                    "status": True,
                    "message": "Portfolio Found!",
                    "details": {
                        "portfolio_id": portfolio["portfolio_id"],
                        "user_id": user_id,
                        "name": portfolio["name"],
                    },
                }
            return {"status": False, "message": "Portfolio Not Found!"}
        if portfolios := General.exclude_metadata(
            jsonable_encoder(crud.portfolio.get_by_user_id(db, user_id))
        ):
            return {
                "status": True,
                "message": "All Portfolios Found!",
                "details": portfolios,
            }
        return {
            "status": False,
            "message": "Portfolio Not Found!",
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.put(
    "/{user_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=UpdatePortfolioResponse,
    response_model_exclude_unset=True,
)
async def update_portfolio(
    user_id: str,
    payload: UpdatePortfolio,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Updates a portfolio details
    """

    try:
        if not is_valid_uuid(user_id):
            raise InvalidUUIDError(
                "Invalid UUID format for user_id uuid",
                status_code=400,
            )
        payload.user_id = user_id
        portfolio = General.exclude_metadata(
            jsonable_encoder(crud.portfolio.update(db, payload.portfolio_id, payload))
        )
        if portfolio:
            details = payload.dict(exclude_unset=True)
            details["portfolio_id"] = payload.portfolio_id
            return {
                "status": True,
                "message": "Successfully updated the portfolio details!",
                "details": details,
            }

        return {
            "status": False,
            "message": "Portfolio Not Found!",
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.delete(
    "/{user_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=DeletePortfolioResponse,
    response_model_exclude_unset=True,
)
async def delete_portfolio(
    user_id: str,
    payload: DeletePortfolio,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Deletes a portfolio details.
    """

    try:
        if not is_valid_uuid(user_id):
            raise InvalidUUIDError(
                "Invalid UUID format for user uuid",
                status_code=400,
            )
        if not is_valid_uuid(payload.portfolio_id):
            raise InvalidUUIDError(
                "Invalid UUID format for portfolio uuid",
                status_code=400,
            )
        portfolio = crud.portfolio.get_by_portfolio_id(db, payload.portfolio_id)
        if portfolio:
            if portfolio := crud.portfolio.delete(db, payload.portfolio_id):
                return {
                    "status": True,
                    "message": "Successfully deleted the portfolio!",
                }

        return {
            "status": False,
            "message": "Portfolio Not Found!",
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)
