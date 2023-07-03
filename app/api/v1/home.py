"""
Home handler module
"""

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def read_root() -> Any:
    """Main handler for the root path"""
    return {"message": "Hello FastAPI!"}
