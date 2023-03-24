"""
Router modules import
"""

from fastapi import APIRouter

from app.api import home

api_router = APIRouter()

# Root router
api_router.include_router(home.router, prefix="/home", tags=["general"])
