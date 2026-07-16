"""Application service layer for uploaded file business logic.

This module coordinates file persistence concerns without handling HTTP,
uploads, authentication, or AI processing directly.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.file import File
from app.models.user import User
from app.repositories.file_repository import FileRepository


class FileService:
    """Encapsulates file-related business logic for the application layer."""

    def __init__(self, repository: FileRepository | None = None) -> None:
        """Initialize the service with a repository dependency."""
        self.repository = repository or FileRepository()

    def upload_file(
        self,
        db: Session,
        user_id: UUID,
        filename: str,
        file_type: str,
        file_path: str,
        file_size: int,
    ) -> File:
        """Create and persist a new file record for a user.

        Args:
            db: Active SQLAlchemy session.
            user_id: UUID of the owning user.
            filename: Original file name.
            file_type: MIME or file type identifier.
            file_path: Stored file path.
            file_size: File size in bytes.

        Returns:
            The saved File model instance.
        """
        file = File(
            user_id=user_id,
            filename=filename,
            file_type=file_type,
            file_path=file_path,
            file_size=file_size,
            scan_status="pending",
        )
        return self.repository.create_file(db, file)

    def get_user_files(self, db: Session, user_id: UUID) -> list[File]:
        """Return all file records belonging to a specific user.

        Args:
            db: Active SQLAlchemy session.
            user_id: UUID of the owning user.

        Returns:
            A list of File objects for the user.
        """
        return self.repository.get_user_files(db, user_id)

    def get_file(self, db: Session, file_id: UUID) -> File:
        """Fetch a file by its identifier.

        Args:
            db: Active SQLAlchemy session.
            file_id: UUID of the file to retrieve.

        Returns:
            The matching File instance.

        Raises:
            ValueError: If no file exists for the given identifier.
        """
        file = self.repository.get_by_id(db, file_id)
        if file is None:
            raise ValueError("File not found")
        return file
    