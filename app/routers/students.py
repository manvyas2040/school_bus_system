from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import require_role
from app.crud import assign_student_to_bus, create_student, get_students
from app.database import get_db
from app.models import Driver
from app.schemas.student import StudentCreate, StudentOut

router = APIRouter(tags=["students"])


@router.post("/students", response_model=StudentOut)
def create_student_endpoint(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    return create_student(db, payload.name.strip(), payload.roll.strip(), payload.bus_id)


@router.get("/students", response_model=dict)
def list_students(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    items, total = get_students(db, page, page_size)
    return {
        "items": [StudentOut.model_validate(item).model_dump() for item in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.put("/students/{student_id}/assign/{bus_id}", response_model=StudentOut)
def assign_student(
    student_id: int,
    bus_id: int,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    return assign_student_to_bus(db, student_id, bus_id)
