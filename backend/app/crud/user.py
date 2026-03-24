"""CRUD operations for user/driver management."""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.exceptions import UserAlreadyExistsException
from app.core.security import hash_password, verify_password
from app.models import Driver


def create_user(db: Session, username: str, password: str, role: str) -> Driver:
    """Create a new user/driver."""
    existing = db.query(Driver).filter(func.lower(Driver.username) == username.lower()).first()
    if existing:
        raise UserAlreadyExistsException()

    user = Driver(username=username, hashed_password=hash_password(password), role=role.lower())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> Driver | None:
    """Authenticate a user with username and password."""
    user = db.query(Driver).filter(Driver.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_username(db: Session, username: str) -> Driver | None:
    """Get a user by username."""
    return db.query(Driver).filter(Driver.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Driver | None:
    """Get a user by ID."""
    return db.query(Driver).filter(Driver.id == user_id).first()
