"""Database initialization utilities."""

from app.database.base import Base
from app.database.session import engine

# Import all models so SQLAlchemy registers them before creating tables.
from app.models.user import User
from app.models.file import File


def init_db() -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)