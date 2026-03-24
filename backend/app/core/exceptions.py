"""Custom exception classes for the application."""

from fastapi import HTTPException, status


class UserAlreadyExistsException(HTTPException):
    """Raised when trying to create a user that already exists."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )


class InvalidCredentialsException(HTTPException):
    """Raised when authentication credentials are invalid."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


class ResourceNotFoundException(HTTPException):
    """Raised when a resource is not found."""

    def __init__(self, resource: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
        )


class InsufficientPermissionsException(HTTPException):
    """Raised when user lacks required permissions."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


class InvalidTokenException(HTTPException):
    """Raised when JWT token is invalid."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
