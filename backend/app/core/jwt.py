"""JWT utility helpers for authentication tokens.

This module centralizes access-token creation and verification using the
application's shared configuration. It does not implement routes, dependencies,
or database access.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT access token.

    Args:
        data: The payload to include in the token.
        expires_delta: Optional custom expiration window. If omitted,
            the configured access token lifetime is used.

    Returns:
        A compact JWT string encoded with the configured algorithm.
    """

    payload = data.copy()

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    expire = datetime.now(timezone.utc) + expires_delta

    payload.update(
        {
            "exp": expire,
        }
    )

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and verify a JWT access token.

    Args:
        token:
            JWT token string received from the client.

    Returns:
        Decoded JWT payload.

    Raises:
        ValueError:
            If the token is expired, invalid, or malformed.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

    except ExpiredSignatureError as exc:
        raise ValueError("Token has expired") from exc

    except JWTError as exc:
        raise ValueError("Invalid token") from exc

    if not isinstance(payload, dict):
        raise ValueError("Invalid token payload")

    return payload