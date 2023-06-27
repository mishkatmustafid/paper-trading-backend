"""
Exceptions module
"""


class PaperTradeCustomError(Exception):
    """Base class for this project's custom exceptions."""


class CustomAuthError(PaperTradeCustomError):
    """
    Custom authentication error class.
    This error is raised if any unauthorised user tries
    to access any endpoints.

    Attributes:
        status_code -- HTTP status code
        message -- explanation of the error
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args)  # is equivalent to -> super().__init__(self.message)
        self.message = str(*args)
        self.status_code = kwargs.get("status_code")


class DatabaseOperationError(PaperTradeCustomError):
    """
    Database operations error class.
    This error is raised if any error occurred during db read/write
    """

    # pylint: disable=unused-argument
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.message = str(*args)


class CustomTokenError(PaperTradeCustomError):
    """
    Custom token error class.
    This error is raised for any error occurred due to invalid/expired token.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.message = str(args)
        self.status_code = kwargs.get("status_code")


class SQLAlchemyObjectNotFoundError(Exception):
    """Row not found"""

    def __init__(self, message, *args, **kwargs):
        # Message must be provided
        self.message = message

        # Init extended exception
        super().__init__(*args, **kwargs)


class InvalidUUIDError(PaperTradeCustomError):
    """
    Custom UUID error class.
    This error is raised if no/invalid uuid is provided
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.message = str(*args)
        self.status_code = kwargs.get("status_code")


class CustomTransferError(PaperTradeCustomError):
    """
    Custom Transfer Error exception
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.message = str(*args)
        self.status_code = kwargs.get("status_code")
