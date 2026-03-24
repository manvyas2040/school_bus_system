from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import require_role
from app.crud import assign_driver_to_bus, create_bus, get_buses
from app.database import get_db
from app.models import Driver
from app.schemas.bus import BusCreate, BusListResponse, BusOut

router = APIRouter(tags=["buses"])


@router.post("/buses", response_model=BusOut)
def create_bus_endpoint(
    payload: BusCreate,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    return create_bus(db, payload.number.strip(), payload.route_id)


@router.get("/buses", response_model=BusListResponse)
def list_buses(
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    items = get_buses(db, search)
    return {"items": items, "total": len(items)}


@router.put("/buses/{bus_id}/assign-driver/{driver_id}", response_model=dict)
def assign_driver(
    bus_id: int,
    driver_id: int,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    driver = assign_driver_to_bus(db, bus_id, driver_id)
    return {
        "id": driver.id,
        "username": driver.username,
        "role": driver.role,
        "bus_id": driver.bus_id,
    }
