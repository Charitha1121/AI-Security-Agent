"""Repository layer for uploaded file database operations.

This module encapsulates persistence and retrieval logic for File records.
It is intentionally limited to database access and does not handle upload,
authentication, or AI processing concerns.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.file import File


class FileRepository:
    """Encapsulates database access for uploaded file records."""

    def create_file(self, db: Session, file: File) -> File:
        """Persist a new File record."""
        db.add(file)
        db.commit()
        db.refresh(file)
        return file

    def get_by_id(self, db: Session, file_id: UUID) -> File | None:
        """Fetch a file by its ID."""
        return db.get(File, file_id)

    def get_user_files(self, db: Session, user_id: UUID) -> list[File]:
        """Fetch all files belonging to a user."""
        statement = (
            select(File)
            .where(File.user_id == user_id)
            .order_by(File.created_at.desc())
        )
        return list(db.scalars(statement).all())

    def update_file(self, db: Session, file: File) -> File:
        """Update an existing file record."""
        db.commit()
        db.refresh(file)
        return file

    def update_scan_status(
        self,
        db: Session,
        file: File,
        status: str,
    ) -> File:
        """Update the scan status of a file."""

        file.scan_status = status

        db.commit()
        db.refresh(file)

        return file

    def delete_file(
        self,
        db: Session,
        file: File,
    ) -> None:
        """Delete a file record."""

        db.delete(file)
        db.commit()