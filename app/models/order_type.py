"""
Order Type model
Enum type of order types
"""

from enum import Enum


class OrderType(Enum):
    """
    Enum class for order types (buy/sell)
    """

    MARKET = "market"
    LIMIT = "limit"
