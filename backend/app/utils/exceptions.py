"""Reusable custom exceptions for AI-related backend operations.

These exceptions provide clear, domain-specific failure points for file handling,
model inference, and report generation without coupling the application to any
specific FastAPI exception handler behavior.
"""


class AIBaseException(Exception):
    """Base exception for all AI Security Agent application errors."""

    pass


class FileValidationException(AIBaseException):
    """Raised when an uploaded file fails validation checks."""

    pass


class UnsupportedFileTypeException(FileValidationException):
    """Raised when a file type is not supported by the application."""

    pass


class ModelInferenceException(AIBaseException):
    """Raised when AI model inference fails unexpectedly."""

    pass


class ReportGenerationException(AIBaseException):
    """Raised when generating a report fails."""

    pass
