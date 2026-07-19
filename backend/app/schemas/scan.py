from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DetectedSecret(BaseModel):
    type: str
    value: str


class ScanResponse(BaseModel):
    id: UUID
    file_id: UUID
    risk_score: int
    verdict: str
    ai_summary: str
    detected_keywords: list[str]
    detected_urls: list[str]
    detected_emails: list[str]
    detected_phones: list[str]
    detected_ips: list[str]
    malicious_urls: list[str]
    detected_secrets: list[DetectedSecret]
    created_at: datetime

    class Config:
        from_attributes = True