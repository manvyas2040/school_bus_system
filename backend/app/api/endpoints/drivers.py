"""Driver management endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud import driver as driver_crud
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models import Driver
from app.schemas.driver import DriverOut

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.get("", response_model=list[DriverOut])
def list_drivers(
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Get all drivers."""
    return driver_crud.get_all_drivers(db)


@router.get("/{driver_id}", response_model=DriverOut)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Get a specific driver by ID."""
    return driver_crud.get_driver_by_id(db, driver_id)


@router.put("/{driver_id}/unassign", status_code=status.HTTP_200_OK)
def unassign_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Unassign a driver from bus."""
    driver = driver_crud.unassign_driver_from_bus(db, driver_id)
    return {
        "id": driver.id,
        "username": driver.username,
        "role": driver.role,
        "bus_id": driver.bus_id,
    }
