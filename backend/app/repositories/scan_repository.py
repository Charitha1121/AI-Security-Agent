from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.scan_result import ScanResult


class ScanRepository:
    """Database operations for scan results."""

    def create_scan(
        self,
        db: Session,
        scan: ScanResult,
    ) -> ScanResult:
        db.add(scan)
        db.commit()
        db.refresh(scan)

        return scan

    def get_by_file_id(
        self,
        db: Session,
        file_id: UUID,
    ) -> Optional[ScanResult]:
        return (
            db.query(ScanResult)
            .filter(
                ScanResult.file_id == file_id
            )
            .order_by(
                ScanResult.created_at.desc()
            )
            .first()
        )

    def get_all(
        self,
        db: Session,
    ) -> list[ScanResult]:
        return (
            db.query(ScanResult)
            .order_by(
                ScanResult.created_at.desc()
            )
            .all()
        )

    def delete_scan(
        self,
        db: Session,
        file_id: UUID,
    ) -> None:
        scans = (
            db.query(ScanResult)
            .filter(
                ScanResult.file_id == file_id
            )
            .all()
        )

        for scan in scans:
            db.delete(scan)

        db.commit()