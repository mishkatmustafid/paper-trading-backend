"""
JWT bearer module
"""

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .auth import verify_token


class JWTBearer(HTTPBearer):
    """
    JWT bearer class
    """

    # pylint: disable=super-with-arguments
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=403, detail={"Invalid authentication scheme."}
            )

        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid or expired token.")
        return credentials.credentials

    @staticmethod
    def verify_jwt(token: str) -> bool:
        return verify_token(token)
