from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.file import File
from app.models.scan import Scan
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    files = (
        db.query(File)
        .filter(File.user_id == current_user.id)
        .all()
    )

    scans = []

    for file in files:

        scan = (
            db.query(Scan)
            .filter(Scan.file_id == file.id)
            .first()
        )

        if scan:
            scans.append(scan)

    total_files = len(files)

    scanned_files = len(scans)

    pending_files = total_files - scanned_files

    high_risk_files = len(
        [
            scan
            for scan in scans
            if scan.verdict == "High Risk"
        ]
    )

    warning_files = len(
        [
            scan
            for scan in scans
            if scan.verdict == "Warning"
        ]
    )

    safe_files = len(
        [
            scan
            for scan in scans
            if scan.verdict == "Safe"
        ]
    )

    average_risk = (
        sum(scan.risk_score for scan in scans) / len(scans)
        if scans
        else 0
    )

    return {
        "total_files": total_files,
        "scanned_files": scanned_files,
        "pending_files": pending_files,
        "high_risk_files": high_risk_files,
        "warning_files": warning_files,
        "safe_files": safe_files,
        "average_risk_score": round(average_risk, 2),
    }