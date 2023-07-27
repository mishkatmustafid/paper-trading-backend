"""
Transaction Status model
Enum type of transaction status
"""

from enum import Enum


class TransactionStatus(Enum):
    """
    Enum class for transaction status (pending/cancelled/fulfilled)
    """

    PENDING = "pending"
    CANCELLED = "cancelled"
    FULFILLED = "fulfilled"
