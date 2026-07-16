"""Authentication service layer for user registration and login.

This module contains the application-facing business logic for authentication.
It coordinates the repository layer and password hashing utilities without
introducing routes, JWT handling, or API-specific concerns.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    """Apply authentication-related business rules for user accounts."""

    def __init__(self, user_repository: UserRepository | None = None) -> None:
        """Initialize the service with a repository dependency."""
        self.user_repository = user_repository or UserRepository()

    def register_user(self, db: Session, user_data: UserCreate) -> User:
        """Register a new user account.

        Args:
            db: Active SQLAlchemy session.
            user_data: Validated registration payload.

        Returns:
            The newly created user record.

        Raises:
            ValueError: If the email address is already registered.
        """
        existing_user = self.user_repository.get_by_email(db, str(user_data.email))
        if existing_user is not None:
            raise ValueError("Email already registered")

        hashed_password = hash_password(user_data.password)
        user = User(
            full_name=user_data.full_name,
            email=str(user_data.email),
            password_hash=hashed_password,
        )

        return self.user_repository.create_user(db, user)

    def authenticate_user(self, db: Session, email: str, password: str) -> User:
        """Authenticate a user with email and password.

        Args:
            db: Active SQLAlchemy session.
            email: User email address.
            password: Plaintext password supplied by the user.

        Returns:
            The authenticated user record.

        Raises:
            ValueError: If no matching user exists or the password is invalid.
        """
        user = self.user_repository.get_by_email(db, email)
        if user is None or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        return user
