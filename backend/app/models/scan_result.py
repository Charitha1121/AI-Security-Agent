from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.file import File


class ScanResult(Base):

    __tablename__ = "scan_results"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    file_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("files.id"),
        nullable=False,
        index=True,
    )

    risk_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    verdict: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    ai_summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    detected_keywords: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    detected_urls: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    detected_emails: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    detected_phones: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    detected_ips: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    malicious_urls: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    detected_secrets: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    file: Mapped["File"] = relationship(
        "File",
        back_populates="scan_result",
    )