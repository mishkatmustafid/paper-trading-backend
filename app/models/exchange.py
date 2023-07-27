"""
Exchange type model
Enum type of exchange (stock/cryptocurrency)
"""

from enum import Enum


class Exchange(Enum):
    """
    Enum class for stock exchange including cryptocurrencies (stock/cryptocurrency)
    """

    NYSE = "nyse"
    LSE = "lse"
    CRYPTOCURRENCY = "cryptocurrency"
