"""
File validation utilities.

This module performs basic security validation on uploaded files before they
are processed by malware scanners or AI analysis.
"""

from __future__ import annotations

from pathlib import Path


class FileValidator:
    """Validate uploaded files."""

    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".csv",
        ".xlsx",
        ".pptx",
    }

    @classmethod
    def validate_extension(cls, filename: str) -> bool:
        """Return True if the extension is allowed."""
        extension = Path(filename).suffix.lower()
        return extension in cls.ALLOWED_EXTENSIONS

    @classmethod
    def validate_size(cls, size: int) -> bool:
        """Return True if file size is acceptable."""
        return size <= cls.MAX_FILE_SIZE

    @classmethod
    def validate(cls, filename: str, size: int) -> None:
        """Validate file before scanning."""

        if not cls.validate_extension(filename):
            raise ValueError("Unsupported file extension")

        if not cls.validate_size(size):
            raise ValueError("File exceeds maximum allowed size")