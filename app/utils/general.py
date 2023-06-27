"""
Helpful scripts for the application.
"""


from typing import List


class General:
    """
    HelpfulScripts class provides
    a collection of helpful scripts for the application.
    """

    def __init__(self):
        pass

    @staticmethod
    def exclude_metadata(data: dict) -> dict:
        """
        Pop meta data from the data.
        """
        if isinstance(data, dict):
            data.pop("password", None)
            data.pop("created_at", None)
            data.pop("updated_at", None)
            data.pop("deleted_at", None)
            data.pop("id", None)
            return data

        if isinstance(data, List):
            for item in data:
                item.pop("password", None)
                item.pop("created_at", None)
                item.pop("updated_at", None)
                item.pop("deleted_at", None)
                item.pop("id", None)
            return data

        return False
