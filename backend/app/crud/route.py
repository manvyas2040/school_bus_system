"""CRUD operations for route management."""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.models import Route


def create_route(db: Session, name: str) -> Route:
    """Create a new route."""
    existing = db.query(Route).filter(func.lower(Route.name) == name.lower()).first()
    if existing:
        raise ValueError("Route already exists")

    route = Route(name=name)
    db.add(route)
    db.commit()
    db.refresh(route)
    return route


def get_all_routes(db: Session) -> list[Route]:
    """Get all routes."""
    return db.query(Route).order_by(Route.id.asc()).all()


def get_route_by_id(db: Session, route_id: int) -> Route:
    """Get a route by ID."""
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise ResourceNotFoundException("Route")
    return route


def update_route(db: Session, route_id: int, name: str) -> Route:
    """Update a route."""
    route = get_route_by_id(db, route_id)

    duplicate = (
        db.query(Route).filter(func.lower(Route.name) == name.lower(), Route.id != route_id).first()
    )
    if duplicate:
        raise ValueError("Route already exists")

    route.name = name
    db.commit()
    db.refresh(route)
    return route


def delete_route(db: Session, route_id: int) -> Route:
    """Delete a route."""
    route = get_route_by_id(db, route_id)
    db.delete(route)
    db.commit()
    return route
