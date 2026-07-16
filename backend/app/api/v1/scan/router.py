from __future__ import annotations

from collections.abc import Generator
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_session
from app.models.user import User
from app.schemas.scan import ScanResponse
from app.services.scan_service import ScanService

router = APIRouter(
    prefix="/scan",
    tags=["AI Scan"],
)


def get_db() -> Generator[Session, None, None]:
    yield from get_session()


def get_scan_service() -> ScanService:
    return ScanService()


@router.post("/{file_id}", response_model=ScanResponse)
def scan_file(
    file_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    service: ScanService = Depends(get_scan_service),
):
    try:
        result = service.scan_file(db, file_id)
        return ScanResponse.model_validate(result)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/{file_id}", response_model=ScanResponse)
def get_scan(
    file_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    service: ScanService = Depends(get_scan_service),
):
    try:
        result = service.get_scan_result(db, file_id)
        return ScanResponse.model_validate(result)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.put("/{file_id}/rescan", response_model=ScanResponse)
def rescan(
    file_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    service: ScanService = Depends(get_scan_service),
):
    try:
        result = service.rescan_file(db, file_id)
        return ScanResponse.model_validate(result)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))