"""Password hashing and JWT helpers for the backend.

This module centralizes password hashing logic using bcrypt through Passlib and
provides JWT creation and verification utilities for future authentication flows.
It intentionally avoids API routes and keeps the scope limited to security helpers.
"""

from datetime import  datetime,timezone, timedelta
from typing import Any, Final

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Placeholder values for future security configuration.
DEFAULT_ALGORITHM: Final[str] = "HS256"
DEFAULT_ACCESS_TOKEN_TTL_MINUTES: Final[int] = 30

# Configure the password hashing context with bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    Args:
        password: The plaintext password to secure.

    Returns:
        A bcrypt-hashed password string.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash.

    Args:
        password: The plaintext password provided by the user.
        hashed_password: The stored hash to compare against.

    Returns:
        True when the password matches the hash, otherwise False.
    """
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict[str, Any]) -> str:
    """Create a signed JWT access token with an expiration claim.

    Args:
        data: The payload to encode into the token.

    Returns:
        A compact JWT string.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_access_token(token: str) -> dict[str, Any]:
    """Validate and decode a JWT access token.

    Args:
        token: The JWT to verify.

    Returns:
        The decoded payload.

    Raises:
        ValueError: If the token is invalid or missing required claims.
        JWTError: If the signature or expiration is invalid.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as exc:
        raise ValueError("Invalid or expired access token") from exc

    if not isinstance(payload, dict):
        raise ValueError("Invalid token payload")

    return payload
