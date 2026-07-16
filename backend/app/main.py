"""FastAPI application entry point for the AI Security Agent backend.

This module initializes the FastAPI application, configures middleware,
and registers API routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database._init_db import init_db
from app.api.v1.auth.router import router as auth_router
from app.api.v1.files.router import router as files_router
from app.core.config import settings
from app.utils.logger import get_logger
from app.api.v1.scan.router import router as scan_router
logger = get_logger(__name__)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend service for the AI Security Agent platform.",
    debug=settings.DEBUG,
)
@app.on_event("startup")
async def startup_event():
    """Initialize the database."""
    init_db()

# Authentication APIs
app.include_router(
    auth_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    scan_router,
    prefix=settings.API_V1_PREFIX,
)
# File management APIs
app.include_router(
    files_router,
    prefix=settings.API_V1_PREFIX,
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
async def read_root() -> dict[str, str]:
    """Return a basic descriptor for the API root endpoint."""

    logger.info("Root endpoint requested")

    return {
        "message": f"{settings.APP_NAME} backend is running."
    }


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Provide service health status."""

    logger.info("Health check requested")

    return {
        "status": "ok"
    }