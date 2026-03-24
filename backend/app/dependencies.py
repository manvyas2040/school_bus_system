"""Dependency injection functions for FastAPI."""

from collections.abc import Callable

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.exceptions import InsufficientPermissionsException, InvalidTokenException
from app.core.security import decode_token
from app.database import get_db
from app.models import Driver

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Driver:
    """Get current authenticated user from JWT token."""
    try:
        payload = decode_token(token)
    except ValueError as exc:
        raise InvalidTokenException() from exc

    if payload.get("type") != "access":
        raise InvalidTokenException()

    username = payload.get("sub")
    if not username:
        raise InvalidTokenException()

    user = db.query(Driver).filter(Driver.username == username).first()
    if not user:
        raise InvalidTokenException()
    return user


def require_role(*roles: str) -> Callable[[Driver], Driver]:
    """Create a dependency that requires specific user roles."""
    allowed = {r.lower() for r in roles}

    def _role_guard(user: Driver = Depends(get_current_user)) -> Driver:
        if user.role.lower() not in allowed:
            raise InsufficientPermissionsException()
        return user

    return _role_guard
