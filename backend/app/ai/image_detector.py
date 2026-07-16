"""
Image detector.

Dummy implementation.
"""

from pathlib import Path


class ImageDetector:
    """Analyze uploaded images."""

    def scan(self, file_path: str) -> dict:

        file_name = Path(file_path).name

        return {
            "risk_score": 5,
            "verdict": "Safe",
            "summary": f"{file_name} scanned successfully. Image appears safe.",
        }