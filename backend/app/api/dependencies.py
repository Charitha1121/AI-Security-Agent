"""Reusable FastAPI dependencies for authentication.

This module contains the dependency layer used by protected endpoints to resolve
an authenticated user from an access token. It keeps HTTP and authentication
concerns separate from the service and repository layers.
"""

from __future__ import annotations

from collections.abc import Generator
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

from app.core.jwt import decode_access_token
from app.database.session import get_session
from app.models.user import User
from app.repositories.user_repository import UserRepository

# OAuth2 scheme for bearer-token authentication.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login"
)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session dependency for request-scoped access."""
    yield from get_session()


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the authenticated user from a bearer token.

    Args:
        token: Bearer token provided in the Authorization header.
        db: Active SQLAlchemy session.

    Returns:
        The authenticated user record.

    Raises:
        HTTPException: If the token is missing, invalid, expired, or if the user
            cannot be found.
    """
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
        )

    try:
        payload = decode_access_token(token)
        user_id_value = payload.get("sub")
        if not user_id_value:
            raise ValueError("Missing user identifier")

        user_id = UUID(str(user_id_value))
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc

    user_repository = UserRepository()
    user = user_repository.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
