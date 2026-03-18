from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud import get_bus_gps, update_bus_gps
from app.database import get_db
from app.models import Driver
from app.schemas.gps import GPSOut, GPSUpdate

router = APIRouter(tags=["gps"])


@router.post("/gps/{bus_id}", response_model=GPSOut)
def update_gps_endpoint(
    bus_id: int,
    payload: GPSUpdate,
    db: Session = Depends(get_db),
    current_user: Driver = Depends(get_current_user),
):
    return update_bus_gps(db, current_user, bus_id, payload.latitude, payload.longitude)


@router.get("/gps/{bus_id}", response_model=GPSOut)
def get_gps(bus_id: int, db: Session = Depends(get_db)):
    return get_bus_gps(db, bus_id)
