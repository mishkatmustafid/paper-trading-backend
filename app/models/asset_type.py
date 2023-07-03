"""
Asset type model
Enum type of asset types (stock/cryptocurrency)
"""

from enum import Enum


class AssetType(Enum):
    """
    Enum class for asset types (stock/cryptocurrency)
    """

    STOCK = "stock"
    CRYPTOCURRENCY = "cryptocurrency"
