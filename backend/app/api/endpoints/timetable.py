"""Timetable endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud import timetable as timetable_crud
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models import Driver
from app.schemas.timetable import TimetableCreate, TimetableOut

router = APIRouter(prefix="/timetable", tags=["timetable"])


@router.get("/{route_id}", response_model=dict)
def get_timetable(route_id: int, db: Session = Depends(get_db)):
    """Get timetable for a specific route."""
    return timetable_crud.get_timetable_for_route(db, route_id)


@router.get("", response_model=list[TimetableOut])
def list_timetables(db: Session = Depends(get_db)):
    """Get all timetables."""
    return timetable_crud.get_all_timetables(db)


@router.post("", response_model=TimetableOut, status_code=status.HTTP_201_CREATED)
def create_timetable(
    payload: TimetableCreate,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Create a new timetable entry."""
    return timetable_crud.create_timetable(
        db, payload.route_id, payload.bus_number, payload.checkpoint, payload.eta_minutes
    )
