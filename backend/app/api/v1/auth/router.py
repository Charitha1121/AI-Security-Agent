"""Authentication API routes.

This module exposes the authentication endpoints for registration and login.
It delegates all application logic to the AuthService and keeps HTTP handling
responsibilities isolated to the router layer.
"""

from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.jwt import create_access_token
from app.database.session import get_session
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service() -> AuthService:
    """Create an AuthService dependency for the router layer."""
    return AuthService()


def get_db() -> Generator[Session, None, None]:
    """Provide a database session dependency for endpoint handlers."""
    yield from get_session()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """Register a new user account through the authentication service."""
    try:
        user = auth_service.register_user(db, user_data)
    except ValueError as exc:
        if str(exc) == "Email already registered":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return UserResponse.model_validate(user)



@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    """Authenticate a user and return a JWT access token."""

    try:
        user = auth_service.authenticate_user(
            db=db,
            email=form_data.username,
            password=form_data.password,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        ) from exc

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_current_user_profile(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Return the authenticated user's profile information."""
    return UserResponse.model_validate(current_user)
