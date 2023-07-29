"""
Assets module. This module contains handlers
related to recent information of symbols
"""

from typing import Any
from fastapi import APIRouter, Depends, Request, Response
from fastapi.encoders import jsonable_encoder
from loguru import logger
from sqlalchemy.orm import Session

from app import crud
from app.auth.bearer import JWTBearer
from app.db.session import db_connection
from app.schemas import CreateAsset, CreateAssetResponse, GetPriceResponse
from app.utils.exceptions import InvalidUUIDError
from app.utils.general import General
from app.utils.handle_error import handle_error
from app.utils.uuid_validation import is_valid_uuid

router = APIRouter()


@router.post(
    "",
    dependencies=[Depends(JWTBearer())],
    response_model=CreateAssetResponse,
    response_model_exclude_unset=True,
)
async def create_data(
    payload: CreateAsset,
    response: Response,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Create new historical market data
    """
    try:
        asset = General.exclude_metadata(
            jsonable_encoder(crud.assets.create(db, payload))
        )
        return {
            "status": True,
            "message": "Successfully created asset",
            "details": asset,
        }

    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


@router.get(
    "",
    dependencies=[Depends(JWTBearer())],
    response_model=GetPriceResponse,
    response_model_exclude_unset=True,
)
async def get_asset(
    response: Response,
    asset_id: str = None,
    name: str = None,
    symbol: str = None,
    db: Session = Depends(db_connection),
) -> Any:
    """
    Get data of an asset
    """
    try:
        if asset_id != None:
            if not is_valid_uuid(asset_id):
                raise InvalidUUIDError(
                    "Make sure to provide user uuid in a valid UUID format.",
                    status_code=400,
                )
            details = crud.assets.get_by_asset_id(db, asset_id)
        elif name != None:
            details = crud.assets.get_by_asset_id(db, name)
        elif symbol != None:
            details = crud.assets.get_by_asset_id(db, symbol)
        else:
            details = crud.assets.get_multi(db)

        if details:
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


# @router.put(
#     "{asset_id}/update",
#     dependencies=[Depends(JWTBearer())],
# )
# async def update_asset(
#     asset_id: str,
#     request: Request,
#     response: Response,
#     db: Session = Depends(db_connection),
# ) -> Any:
#     """
#     Updates asset info
#     """
#     try:
#         if not is_valid_uuid(asset_id):
#             raise InvalidUUIDError(
#                 "Make sure to provide user uuid in a valid UUID format.",
#                 status_code=400,
#             )

#     except Exception as err:
#         logger.error(err)
#         return handle_error.send_error(err, response)
