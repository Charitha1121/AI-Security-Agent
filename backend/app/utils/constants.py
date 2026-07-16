"""Application-wide constants for the AI Security Agent backend.

These constants centralize file type support, upload limits, and risk level
labels so they can be reused consistently across services and validators.
"""

from typing import Final

# Environment names used by configuration and runtime checks.
APP_ENVIRONMENT_DEVELOPMENT: Final[str] = "development"
APP_ENVIRONMENT_PRODUCTION: Final[str] = "production"
APP_ENVIRONMENT_TEST: Final[str] = "test"

# Supported file extensions for uploaded content.
SUPPORTED_IMAGE_EXTENSIONS: Final[set[str]] = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
SUPPORTED_VIDEO_EXTENSIONS: Final[set[str]] = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
SUPPORTED_AUDIO_EXTENSIONS: Final[set[str]] = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}
SUPPORTED_TEXT_EXTENSIONS: Final[set[str]] = {".txt", ".csv", ".json", ".log", ".md"}

# Maximum upload size in bytes for incoming files.
MAX_UPLOAD_SIZE_BYTES: Final[int] = 50 * 1024 * 1024  # 50 MB

# Risk classification labels used by analysis and reporting modules.
RISK_LEVELS: Final[tuple[str, str, str]] = ("LOW", "MEDIUM", "HIGH")
