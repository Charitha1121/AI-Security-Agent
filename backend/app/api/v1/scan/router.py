from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_user,
    get_db,
)

from app.models.user import User
from app.models.file import File
from app.models.scan_result import ScanResult

from app.schemas.scan import ScanResponse
from app.services.scan_service import ScanService


router = APIRouter()

scan_service = ScanService()


# ============================================================
# GET SCAN HISTORY
# ============================================================

@router.get(
    "/history",
    response_model=list[ScanResponse],
)
def get_scan_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    scans = (
        db.query(ScanResult)
        .join(
            File,
            ScanResult.file_id == File.id,
        )
        .filter(
            File.user_id == current_user.id
        )
        .order_by(
            ScanResult.created_at.desc()
        )
        .all()
    )

    # Normalize old malformed detected_phones data
    for scan in scans:

        normalized_phones = []

        for item in scan.detected_phones or []:

            if isinstance(item, list):

                normalized_phones.extend(
                    str(phone)
                    for phone in item
                    if phone
                )

            else:

                normalized_phones.append(
                    str(item)
                )

        scan.detected_phones = normalized_phones

    return scans


# ============================================================
# SCAN FILE
# ============================================================

@router.post(
    "/{file_id}",
    response_model=ScanResponse,
)
def scan_file(
    file_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:

        result = scan_service.scan_file(
            db,
            file_id,
        )

        return result["scan"]

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


# ============================================================
# GET SCAN RESULT
# ============================================================

@router.get(
    "/{file_id}",
    response_model=ScanResponse,
)
def get_scan(
    file_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    scan = scan_service.get_scan_result(
        db,
        file_id,
    )

    if scan is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan result not found",
        )

    return scan


# ============================================================
# RESCAN FILE
# ============================================================

@router.put(
    "/{file_id}/rescan",
    response_model=ScanResponse,
)
def rescan_file(
    file_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:

        result = scan_service.rescan_file(
            db,
            file_id,
        )

        return result["scan"]

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )