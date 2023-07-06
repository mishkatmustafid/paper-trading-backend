"""
Market Data Historical module. This module
contains handlers related to fetch historical data of
symbols
"""

from fastapi import APIRouter, Depends, Response
from loguru import logger
from sqlalchemy.orm import Session

from app import crud
from app.auth.bearer import JWTBearer
from app.db.session import db_connection
from app.schemas import GetPriceResponse
from app.utils.handle_error import handle_error

router = APIRouter()


@router.get(
    "",
    dependencies=[Depends(JWTBearer())],
    response_model=GetPriceResponse,
    response_model_exclude_unset=True,
)
async def get_price(
    symbol: str,
    response: Response,
    db: Session = Depends(db_connection),
):
    """
    Get price of a symbol
    """
    try:
        if details := crud.market_data.get_price_by_symbol(db, symbol):
            return {
                "status": True,
                "message": "Successfully got the price!",
                "details": details,
            }
        return {
            "status": False,
            "message": "No price found for the given symbol!",
            "details": {},
        }
    except Exception as err:
        logger.error(err)
        return handle_error.send_error(err, response)


# @router.get(
#     "/{symbol}/details",
#     dependencies=[Depends(JWTBearer())],
#     response_model=GetDetailsResponse,
#     response_model_exclude_unset=True,
# )
# def get_details(
#     symbol: str,
#     response: Response,
#     db: Session = Depends(db_connection),
# ) -> Any:
#     """
#     Get details of a symbol
#     """
#     try:

#           details = crud.market_data.get_details_by_symbol(db, symbol)

#           return {
#               "status": True,
#               "message": "Successfully got the details!",
#               "details": {
#                   "symbol": symbol,
#                   "open": details["open"],
#                   "high": details["high"],
#                   "low": details["low"],
#                   "volume": details["volume"],
#                   "52_week_high": details["52_week_high"],
#                   "52_week_low": details["52_week_low"],
#                   "market_cap": details["market_cap"],
#               },
#           }
#     except Exception as err:
#         logger.error(err)
#         return handle_error.send_error(err, response)


# @router.get(
#     "/klines",
#     dependencies=[Depends(JWTBearer())],
#     response_model=GetKlinesResponse,
#     response_model_exclude_unset=True,
# )
# def get_details(
#     symbol: str,
#     interval: str,
#     start_time: int,
#     end_time: int,
#     limit: int,
#     response: Response,
#     db: Session = Depends(db_connection),
# ) -> Any:
#     """
#     Get klines of a symbol
#     """
#     try:
#         klines = crud.market_data.get_klines(
#             db, symbol, interval, start_time, end_time, limit
#         )

#         return {
#             "status": True,
#             "message": "Successfully got the klines!",
#             "details": {
#                 "symbol": symbol,
#                 "interval": interval,
#                 "limit": limit,
#                 "klines": klines,
#             },
#         }
#     except Exception as err:
#         logger.error(err)
#         return handle_error.send_error(err, response)
