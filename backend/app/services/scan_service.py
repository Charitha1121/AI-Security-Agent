from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.pdf_analyzer import PDFAnalyzer
from app.models.scan_result import ScanResult
from app.repositories.file_repository import FileRepository
from app.repositories.scan_repository import ScanRepository


class ScanService:
    """Service layer for file scanning."""

    def __init__(self) -> None:
        self.file_repository = FileRepository()
        self.scan_repository = ScanRepository()

    def scan_file(self, db: Session, file_id: UUID) -> ScanResult:
        """Analyze a file and save the scan result."""

        file = self.file_repository.get_by_id(db, file_id)

        if file is None:
            raise ValueError("File not found")

        analysis = PDFAnalyzer.analyze(file.file_path)

        scan_result = ScanResult(
            file_id=file.id,
            risk_score=analysis["risk_score"],
            verdict=analysis["verdict"],
            ai_summary=analysis["ai_summary"],
        )

        scan_result = self.scan_repository.create_scan(
            db,
            scan_result,
        )

        file.scan_status = "completed"
        db.commit()

        return scan_result

    def get_scan_result(self, db: Session, file_id: UUID):
        """Return the latest scan result for a file."""
        return self.scan_repository.get_by_file_id(db, file_id)

    def rescan_file(self, db: Session, file_id: UUID):
        """Delete the old scan result and scan again."""

        self.scan_repository.delete_scan(db, file_id)

        return self.scan_file(db, file_id)