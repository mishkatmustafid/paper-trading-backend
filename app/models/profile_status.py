"""
Profile status module
"""

from enum import Enum


class ProfileStatus(Enum):
    """
    Enum class for different profile statuses
    """

    SIGNUP = "signup"
    SIGNUP_CONFIRMED = "signup_confirmed"
    BLOCKED = "blocked"
