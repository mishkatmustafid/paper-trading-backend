"""
Router modules import
"""

from fastapi import APIRouter

from app.api.v1 import (
    home,
    user,
    portfolio,
    portfolio_stock,
    transaction,
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
