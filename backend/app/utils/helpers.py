"""Helper functions for common operations."""

from datetime import datetime, timezone


def get_utc_now() -> datetime:
    """Get current UTC time with timezone info."""
    return datetime.now(timezone.utc)
