"""Route management endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud import route as route_crud
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models import Driver
from app.schemas.route import RouteCreate, RouteOut

router = APIRouter(prefix="/routes", tags=["routes"])


@router.post("", response_model=RouteOut, status_code=status.HTTP_201_CREATED)
def create_route(
    payload: RouteCreate,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Create a new route."""
    return route_crud.create_route(db, payload.name.strip())


@router.get("", response_model=list[RouteOut])
def list_routes(db: Session = Depends(get_db)):
    """Get all routes."""
    return route_crud.get_all_routes(db)


@router.get("/{route_id}", response_model=RouteOut)
def get_route(
    route_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific route by ID."""
    return route_crud.get_route_by_id(db, route_id)


@router.put("/{route_id}", response_model=RouteOut)
def update_route(
    route_id: int,
    payload: RouteCreate,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Update a route."""
    return route_crud.update_route(db, route_id, payload.name.strip())


@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Delete a route."""
    route_crud.delete_route(db, route_id)
