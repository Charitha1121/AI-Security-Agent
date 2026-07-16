"""
Pydantic schemas for AI scan results.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ScanResponse(BaseModel):
    """Response returned after scanning a file."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    file_id: UUID
    risk_score: int
    verdict: str
    ai_summary: str
    created_at: datetime