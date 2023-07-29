"""
Router modules import
"""

from fastapi import APIRouter

from app.api.v1 import (
    assets,
    home,
    market_data_historical,
    portfolio,
    portfolio_stock,
    transaction,
    user,
)

api_router = APIRouter()

# Root router
api_router.include_router(home.router, prefix="/home", tags=["general"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(
    transaction.router, prefix="/transaction", tags=["transaction"]
)
api_router.include_router(
    portfolio_stock.router, prefix="/portfolio_stock", tags=["portfoliostocks"]
)
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(
    market_data_historical.router,
    prefix="/marketdata",
    tags=["marketdatahistorical"],
)
