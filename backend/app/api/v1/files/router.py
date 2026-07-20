"""File management API routes.

This module provides endpoints for uploading files and retrieving
user-uploaded file records. Business logic is delegated to FileService.
"""

from __future__ import annotations
from app.scanners.file_validator import FileValidator
import os
import uuid
from collections.abc import Generator
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_session
from app.models.user import User
from app.schemas.file import FileResponse
from app.services.file_service import FileService
router = APIRouter()

UPLOAD_DIRECTORY = Path("uploads")


def get_db() -> Generator[Session, None, None]:
    """Provide database session dependency."""
    yield from get_session()


def get_file_service() -> FileService:
    """Provide FileService dependency."""
    return FileService()


@router.post(
    "/upload",
    response_model=FileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
) -> FileResponse:
    """Upload a file and create a database record."""

    allowed_types = [
    "image/",
    "video/",
    "audio/",
    "text/",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/zip",
    "application/x-zip-compressed",
]
    content_type = file.content_type or ""

    if not any(
        content_type.startswith(file_type)
        for file_type in allowed_types
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type",
        )

    UPLOAD_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    file_path = UPLOAD_DIRECTORY / unique_filename

    content = await file.read()
    file_size = len(content)
    FileValidator.validate(
    filename=file.filename,
    size=file_size,
)
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    saved_file = file_service.upload_file(
    db=db,
    user_id=current_user.id,
    filename=file.filename,
    file_type=file.content_type or "application/octet-stream",
    file_path=str(file_path),
    file_size=file_size,
)

    return FileResponse.model_validate(saved_file)


@router.get(
    "/",
    response_model=list[FileResponse],
)
def get_user_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
) -> list[FileResponse]:
    """Return all files uploaded by the current user."""

    files = file_service.get_user_files(
        db,
        current_user.id,
    )

    return [
        FileResponse.model_validate(file)
        for file in files
    ]


@router.get(
    "/{file_id}",
    response_model=FileResponse,
)
def get_file(
    file_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
) -> FileResponse:
    """Return a single uploaded file record."""

    file = file_service.get_file(
        db,
        file_id,
    )

    if file.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return FileResponse.model_validate(file)