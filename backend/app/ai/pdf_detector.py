"""
PDF detector.

Dummy implementation.
"""

from pathlib import Path


class PDFDetector:
    """Analyze uploaded PDFs."""

    def scan(self, file_path: str) -> dict:

        file_name = Path(file_path).name

        return {
            "risk_score": 8,
            "verdict": "Safe",
            "summary": f"{file_name} scanned successfully. No suspicious content detected.",
        }