from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import get_timetable_for_route
from app.database import get_db
from app.schemas.timetable import TimetableResponse

router = APIRouter(tags=["timetable"])


@router.get("/timetable/{route_id}", response_model=TimetableResponse)
def get_timetable(route_id: int, db: Session = Depends(get_db)):
    return get_timetable_for_route(db, route_id)
