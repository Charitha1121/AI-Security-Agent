from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database._init_db import init_db
from app.api.v1.auth.router import router as auth_router
from app.api.v1.files.router import router as files_router
from app.api.v1.scan.router import router as scan_router
from app.core.config import settings
from app.utils.logger import get_logger


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


# Scan APIs
app.include_router(
    scan_router,
    prefix=f"{settings.API_V1_PREFIX}/scan",
    tags=["Scan"],
)


# File management APIs
app.include_router(
    files_router,
    prefix=f"{settings.API_V1_PREFIX}/files",
    tags=["Files"],
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
    return {
        "message": f"{settings.APP_NAME} backend is running."
    }


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {
        "status": "ok"
    }