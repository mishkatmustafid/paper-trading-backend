"""Application server module"""

import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from loguru import logger

from app.core import settings
from app.api.v1 import api_router

app = FastAPI(title=settings.PROJECT_NAME)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

VALID_ENVS = ["local", "dev", "stg", "prd"]
ENV = settings.ENVIRONMENT

if ENV not in VALID_ENVS:
    logger.error(
        f"{ENV} is not a valid value for environment, supported values: {VALID_ENVS}"
    )
    sys.exit(1)

logger.info(f"ENVIRONMENT is set to {ENV} and running on {settings.PORT}")


# For local/dev/stg env:
#   > docs_url, redoc_url, and openapi_url is set to None. And these
#   endpoints are overridden as following. API documentation can be
#   browsed using basic auth.

# For production env:
#   > API documentation urls are disabled
# ----------------------------------------------------------------
if ENV in VALID_ENVS[:3]:
    # pylint: disable=unused-argument

    @app.get("/", include_in_schema=False)
    async def get_root():
        return {
            "status": True,
            "message": "Welcome to the Tiger Trade API service. Authenticate to proceed further.",
        }

    @app.get("/apidoc", include_in_schema=False)
    async def get_swagger_documentation():
        return get_swagger_ui_html(
            openapi_url="/openapi.json", title=settings.PROJECT_NAME
        )

    @app.get("/redoc", include_in_schema=False)
    async def get_redoc_documentation():
        return get_redoc_html(openapi_url="/openapi.json", title=settings.PROJECT_NAME)

    @app.get("/openapi.json", include_in_schema=False)
    async def openapi():
        return get_openapi(
            title=settings.PROJECT_NAME, version=settings.VERSION, routes=app.routes
        )


def init_server() -> None:
    """
    Configure logging and log format.
    Spin up the server.
    """

    # Run the server
    uvicorn.run(
        "app.server:app",
        host="127.0.0.0",
        port=int(settings.PORT),
        reload=True,
    )
