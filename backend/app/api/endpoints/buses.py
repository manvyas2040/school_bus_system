"""Bus management endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.crud import bus as bus_crud
from app.crud import driver as driver_crud
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models import Driver
from app.schemas.bus import BusCreate, BusListResponse, BusOut

router = APIRouter(prefix="/buses", tags=["buses"])


@router.post("", response_model=BusOut, status_code=status.HTTP_201_CREATED)
def create_bus(
    payload: BusCreate,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Create a new bus."""
    return bus_crud.create_bus(db, payload.number.strip(), payload.route_id)


@router.get("", response_model=BusListResponse)
def list_buses(
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """Get all buses with optional search."""
    items = bus_crud.get_buses(db, search)
    return {"items": items, "total": len(items)}


@router.get("/{bus_id}", response_model=BusOut)
def get_bus(
    bus_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific bus by ID."""
    return bus_crud.get_bus_by_id(db, bus_id)


@router.put("/{bus_id}/assign-driver/{driver_id}", response_model=dict)
def assign_driver(
    bus_id: int,
    driver_id: int,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Assign a driver to a bus."""
    driver = driver_crud.assign_driver_to_bus(db, bus_id, driver_id)
    return {
        "id": driver.id,
        "username": driver.username,
        "role": driver.role,
        "bus_id": driver.bus_id,
    }


@router.delete("/{bus_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bus(
    bus_id: int,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Delete a bus."""
    bus_crud.delete_bus(db, bus_id)
