"""
UUID validation module
"""

from uuid import UUID


def is_valid_uuid(uuid_str: str) -> bool:
    try:
        UUID(str(uuid_str))
        return True
    except ValueError:
        return False
