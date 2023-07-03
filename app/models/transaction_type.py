"""
Transaction Type model
Enum type of transaction types
"""

from enum import Enum


class TransactionType(Enum):
    """
    Enum class for transaction types (buy/sell)
    """

    BUY = "buy"
    SELL = "sell"
