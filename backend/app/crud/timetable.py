"""CRUD operations for timetable management."""

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.models import Route, Timetable


def get_timetable_for_route(db: Session, route_id: int) -> dict:
    """Get timetable for a specific route."""
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise ResourceNotFoundException("Route")

    timetables = db.query(Timetable).filter(Timetable.route_id == route_id).all()

    entries = [
        {
            "bus_number": t.bus_number,
            "checkpoint": t.checkpoint,
            "eta_minutes": t.eta_minutes,
        }
        for t in timetables
    ]

    return {
        "route_id": route.id,
        "route_name": route.name,
        "entries": entries,
    }


def get_all_timetables(db: Session) -> list[Timetable]:
    """Get all timetables."""
    return db.query(Timetable).order_by(Timetable.id.asc()).all()


def create_timetable(
    db: Session, route_id: int, bus_number: str, checkpoint: str, eta_minutes: int
) -> Timetable:
    """Create a new timetable entry."""
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise ResourceNotFoundException("Route")

    timetable = Timetable(route_id=route_id, bus_number=bus_number, checkpoint=checkpoint, eta_minutes=eta_minutes)
    db.add(timetable)
    db.commit()
    db.refresh(timetable)
    return timetable
