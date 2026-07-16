"""Pydantic schemas for uploaded file operations.

This module defines request and response schemas for file management.
It only handles data validation and serialization.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FileResponse(BaseModel):
    """Schema returned when displaying uploaded file information."""

    id: UUID
    user_id: UUID
    filename: str
    file_type: str
    file_path: str
    file_size: int
    scan_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FileUpdate(BaseModel):
    """Schema for updating file scan status."""

    scan_status: str | None = None