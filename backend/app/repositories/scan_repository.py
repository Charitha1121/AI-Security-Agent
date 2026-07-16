from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.scan_result import ScanResult


class ScanRepository:
    """Repository for scan results."""

    def create_scan(
        self,
        db: Session,
        scan_result: ScanResult,
    ) -> ScanResult:
        """Save a new scan result."""

        db.add(scan_result)
        db.commit()
        db.refresh(scan_result)

        return scan_result

    def get_by_file_id(
        self,
        db: Session,
        file_id: UUID,
    ) -> ScanResult | None:
        """Return the latest scan result for a file."""

        stmt = (
            select(ScanResult)
            .where(ScanResult.file_id == file_id)
            .order_by(ScanResult.created_at.desc())
        )

        return db.scalar(stmt)

    def delete_scan(
        self,
        db: Session,
        file_id: UUID,
    ) -> None:
        """Delete the existing scan result for a file."""

        scan = self.get_by_file_id(db, file_id)

        if scan:
            db.delete(scan)
            db.commit()