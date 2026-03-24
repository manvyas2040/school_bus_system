"""CRUD operations for GPS tracking."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.exceptions import InsufficientPermissionsException, ResourceNotFoundException
from app.models import GPS, Driver


def update_bus_gps(db: Session, user: Driver, bus_id: int, latitude: float, longitude: float) -> GPS:
    """Update GPS location for a bus."""
    if user.role.lower() != "driver":
        raise InsufficientPermissionsException()
    if user.bus_id != bus_id:
        raise InsufficientPermissionsException()

    gps = db.query(GPS).filter(GPS.bus_id == bus_id).first()
    if not gps:
        raise ResourceNotFoundException("GPS")

    gps.latitude = latitude
    gps.longitude = longitude
    gps.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(gps)
    return gps


def get_bus_gps(db: Session, bus_id: int) -> GPS:
    """Get GPS location of a bus."""
    gps = db.query(GPS).filter(GPS.bus_id == bus_id).first()
    if not gps:
        raise ResourceNotFoundException("GPS")
    return gps


def get_all_gps(db: Session) -> list[GPS]:
    """Get all GPS records."""
    return db.query(GPS).order_by(GPS.id.asc()).all()
