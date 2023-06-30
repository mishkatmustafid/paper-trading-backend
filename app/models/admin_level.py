"""
Admin level model.
Enum type of different level of admins.
"""

from enum import Enum


class AdminLevel(Enum):
    """
    Enum class for different admin levels
    """

    admin = 3
    teacher = 2
    user = 1

    @classmethod
    def is_admin(cls, level: str) -> bool:
        return level in [cls.tt_admin.value]

    def __str__(self):
        return self.name
