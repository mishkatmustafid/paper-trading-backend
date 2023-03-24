"""
Core application configuration module
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Paper Trade Backend API Service"
    PORT: str = "9000"
    ENVIRONMENT: str
    DB_URL: str
    MIGRATION_SCRIPT_LOCATION: str

    # JWT vars
    SIGNING_KEY: str
    SIGNING_ALGORITHM: str
    VALIDATION_PERIOD: str
    TOKEN_ISSUER: str
    TOKEN_AUDIENCE: str

    # Basic auth vars
    BA_API_DOC_USERNAME: str
    BA_API_DOC_PASSWORD: str

    # SUPER ADMIN USER
    SUPER_ADMIN_USER: str
    SUPER_ADMIN_PW: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
