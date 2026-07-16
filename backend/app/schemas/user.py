"""Pydantic schemas for user-related request and response payloads.

These models define the validation and serialization rules for the user domain.
They are intentionally limited to schema definitions and do not include CRUD logic.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """Schema for creating a new user account."""

    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        """Trim surrounding whitespace from the full name."""
        return value.strip()


class UserLogin(BaseModel):
    """Schema for authenticating an existing user."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)


class UserResponse(BaseModel):
    """Schema for returning a user record to clients."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    created_at: datetime


class UserUpdate(BaseModel):
    """Schema for partially updating a user's profile."""

    full_name: str | None = Field(default=None, min_length=1, max_length=255)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str | None) -> str | None:
        """Trim and normalize the optional full name value."""
        if value is None:
            return None
        return value.strip()
