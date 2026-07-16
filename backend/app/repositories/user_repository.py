"""Repository layer for user database operations.

This module contains SQLAlchemy-based data access methods for the User model.
It intentionally focuses on persistence and retrieval only and does not handle
password hashing, JWT creation, or application logic.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Encapsulates database access for user records."""

    def get_by_email(self, db: Session, email: str) -> User | None:
        """Fetch a user by email address.

        Args:
            db: Active SQLAlchemy session.
            email: User email address to look up.

        Returns:
            The matching user record, if one exists.
        """
        return db.scalar(select(User).where(User.email == email))

    def get_by_id(self, db: Session, user_id: UUID) -> User | None:
        """Fetch a user by primary key.

        Args:
            db: Active SQLAlchemy session.
            user_id: The UUID of the user to retrieve.

        Returns:
            The matching user record, if one exists.
        """
        return db.get(User, user_id)

    def create_user(self, db: Session, user: User) -> User:
        """Insert a new user record into the database.

        Args:
            db: Active SQLAlchemy session.
            user: User model instance to persist.

        Returns:
            The persisted user instance.
        """
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
