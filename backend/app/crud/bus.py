"""CRUD operations for bus management."""

from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.models import Bus, GPS, Route


def create_bus(db: Session, number: str, route_id: int) -> Bus:
    """Create a new bus."""
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise ResourceNotFoundException("Route")

    duplicate = db.query(Bus).filter(func.lower(Bus.number) == number.lower()).first()
    if duplicate:
        raise ValueError("Bus number already exists")

    bus = Bus(number=number, route_id=route_id)
    db.add(bus)
    db.flush()

    gps = GPS(bus_id=bus.id, latitude=0.0, longitude=0.0, updated_at=datetime.now(timezone.utc))
    db.add(gps)
    db.commit()
    db.refresh(bus)
    return bus


def get_buses(db: Session, search: str | None = None) -> list[Bus]:
    """Get all buses with optional search."""
    query = db.query(Bus)
    if search:
        query = query.filter(func.lower(Bus.number).contains(search.lower()))
    return query.order_by(Bus.id.asc()).all()


def get_bus_by_id(db: Session, bus_id: int) -> Bus:
    """Get a bus by ID."""
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        raise ResourceNotFoundException("Bus")
    return bus


def delete_bus(db: Session, bus_id: int) -> Bus:
    """Delete a bus."""
    bus = get_bus_by_id(db, bus_id)
    db.delete(bus)
    db.commit()
    return bus


def update_bus(db: Session, bus_id: int, number: str | None = None, route_id: int | None = None) -> Bus:
    """Update bus information."""
    bus = get_bus_by_id(db, bus_id)

    if number:
        duplicate = (
            db.query(Bus)
            .filter(func.lower(Bus.number) == number.lower(), Bus.id != bus_id)
            .first()
        )
        if duplicate:
            raise ValueError("Bus number already exists")
        bus.number = number

    if route_id:
        route = db.query(Route).filter(Route.id == route_id).first()
        if not route:
            raise ResourceNotFoundException("Route")
        bus.route_id = route_id

    db.commit()
    db.refresh(bus)
    return bus
