from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.pdf_analyzer import PDFAnalyzer
from app.models.file import File
from app.models.scan_result import ScanResult
from app.repositories.file_repository import FileRepository
from app.repositories.scan_repository import ScanRepository


class ScanService:
    """Service layer for file scanning."""

    def __init__(self) -> None:
        self.file_repository = FileRepository()
        self.scan_repository = ScanRepository()

    def scan_file(
        self,
        db: Session,
        file_id: UUID,
    ):
        file = self.file_repository.get_by_id(
            db,
            file_id,
        )

        if file is None:
            raise ValueError("File not found")

        analysis = PDFAnalyzer.analyze(
            file.file_path
        )

        scan = ScanResult(
            file_id=file.id,
            risk_score=analysis.get(
                "risk_score",
                0,
            ),
            verdict=analysis.get(
                "verdict",
                "Unknown",
            ),
            ai_summary=analysis.get(
                "ai_summary",
                "",
            ),
            detected_keywords=analysis.get(
                "detected_keywords",
                [],
            ),
            detected_urls=analysis.get(
                "detected_urls",
                [],
            ),
            detected_emails=analysis.get(
                "detected_emails",
                [],
            ),
            detected_phones=analysis.get(
                "detected_phones",
                [],
            ),
            detected_ips=analysis.get(
                "detected_ips",
                [],
            ),
            malicious_urls=analysis.get(
                "malicious_urls",
                [],
            ),
            detected_secrets=analysis.get(
                "detected_secrets",
                [],
            ),
        )

        scan = self.scan_repository.create_scan(
            db,
            scan,
        )

        file.scan_status = "completed"

        db.commit()
        db.refresh(scan)

        return {
            "scan": scan,
            "analysis": analysis,
        }

    def get_scan_result(
        self,
        db: Session,
        file_id: UUID,
    ):
        return self.scan_repository.get_by_file_id(
            db,
            file_id,
        )

    def rescan_file(
        self,
        db: Session,
        file_id: UUID,
    ):
        file = self.file_repository.get_by_id(
            db,
            file_id,
        )

        if file is None:
            raise ValueError(
                "File not found"
            )

        self.scan_repository.delete_scan(
            db,
            file_id,
        )

        return self.scan_file(
            db,
            file_id,
        )

    def get_user_scan_history(
        self,
        db: Session,
        user_id: UUID,
    ):
        return (
            db.query(ScanResult)
            .join(
                File,
                ScanResult.file_id == File.id,
            )
            .filter(
                File.user_id == user_id
            )
            .order_by(
                ScanResult.created_at.desc()
            )
            .all()
        )