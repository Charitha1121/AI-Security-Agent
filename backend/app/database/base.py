"""SQLAlchemy declarative base for future ORM models.

This module provides the single shared base class that all database models will
inherit from. No model definitions are created here yet.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base used by all SQLAlchemy models."""

    pass
