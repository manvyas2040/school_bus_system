"""GPS tracking endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import gps as gps_crud
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Driver
from app.schemas.gps import GPSOut, GPSUpdate

router = APIRouter(prefix="/gps", tags=["gps"])


@router.post("/{bus_id}", response_model=GPSOut)
def update_gps(
    bus_id: int,
    payload: GPSUpdate,
    db: Session = Depends(get_db),
    current_user: Driver = Depends(get_current_user),
):
    """Update GPS location for a bus."""
    return gps_crud.update_bus_gps(db, current_user, bus_id, payload.latitude, payload.longitude)


@router.get("/{bus_id}", response_model=GPSOut)
def get_gps(bus_id: int, db: Session = Depends(get_db)):
    """Get GPS location of a bus."""
    return gps_crud.get_bus_gps(db, bus_id)


@router.get("", response_model=list[GPSOut])
def get_all_gps(db: Session = Depends(get_db)):
    """Get all GPS records."""
    return gps_crud.get_all_gps(db)
