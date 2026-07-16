"""
AI Scanner.

Coordinates different scanners based on the uploaded file type.
"""

from pathlib import Path

from app.ai.image_detector import ImageDetector
from app.ai.pdf_detector import PDFDetector


class AIScanner:
    """Main AI Scanner."""

    def __init__(self) -> None:
        self.pdf_detector = PDFDetector()
        self.image_detector = ImageDetector()

    def scan(self, file_path: str) -> dict:
        """
        Scan a file.

        Returns:
            {
                "risk_score": int,
                "verdict": str,
                "summary": str
            }
        """

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return self.pdf_detector.scan(file_path)

        if extension in {
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".gif",
        }:
            return self.image_detector.scan(file_path)

        return {
            "risk_score": 0,
            "verdict": "Unsupported",
            "summary": "Unsupported file type.",
        }