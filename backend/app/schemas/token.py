"""Pydantic schemas for JWT authentication payloads.

These models are used to validate and serialize token-related data for the
authentication flow. They remain focused on data validation and do not contain
business logic, database access, or route definitions.
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    """Schema returned when issuing an access token."""

    access_token: str = Field(..., description="The signed JWT access token")
    token_type: str = Field(default="bearer", description="The token type")


class TokenData(BaseModel):
    """Schema representing the decoded claims carried by a JWT."""

    model_config = ConfigDict(from_attributes=True)

    user_id: UUID | None = Field(default=None, description="The authenticated user's UUID")
