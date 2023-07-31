"""
Market Data Historical module. This module
contains handlers related to fetch historical data of
symbols
"""

from typing import Any

from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from loguru import logger
from sqlalchemy.orm import Session

from app import crud
from app.auth.bearer import JWTBearer
from app.db.session import db_connection
from app.schemas import (
    CreateMarketDataHistorical,
    CreateMarketDataHistoricalResponse,
    GetAllDataResponse,
)
from app.utils.exceptions import InvalidUUIDError
from app.utils.general import General
from app.utils.handle_error import handle_error
from app.utils.uuid_validation import is_valid_uuid

router = APIRouter()


@router.post(
    "",
    dependencies=[Depends(JWTBearer())],
    response_model=CreateMarketDataHistoricalResponse,
    response_model_exclude_unset=True,
)
async def create_data(
    payload: CreateMarketDataHistorical,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Create new historical market data
    """
    try:
        market_data_historical = General.exclude_metadata(
            jsonable_encoder(crud.market_data_historical.create(db, payload))
        )
        return {
            "status": True,
            "message": "Successfully created marketdata historical",
            "details": market_data_historical,
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.get(
    "/{asset_id}",
    dependencies=[Depends(JWTBearer())],
    response_model=GetAllDataResponse,
    response_model_exclude_unset=True,
)
async def get_info(
    asset_id: str,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Get data of an asset
    """
    try:
        if not is_valid_uuid(asset_id):
            raise InvalidUUIDError(
                "Make sure to provide user uuid in a valid UUID format.",
                status_code=400,
            )
        if details := crud.market_data_historical.get_by_asset_id(db, asset_id):
            details = General.exclude_metadata(jsonable_encoder(details))
            print("Endpoint")
            print(details)
            return {
                "status": True,
                "message": "Successfully got the asset data!",
                "details": details,
            }
        return {
            "status": False,
            "message": "No data found for the given asset!",
            "details": {},
        }
    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)
