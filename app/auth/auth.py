import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core import settings

security = HTTPBasic()


def get_apidoc_username(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Returns apidoc username if credentials are valid.
    """
    correct_username = secrets.compare_digest(
        credentials.username, settings.BA_API_DOC_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.BA_API_DOC_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
