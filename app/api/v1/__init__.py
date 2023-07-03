"""
Router modules import
"""

from fastapi import APIRouter

from app.api.v1 import home, user

api_router = APIRouter()

# Root router
api_router.include_router(home.router, prefix="/home", tags=["general"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
