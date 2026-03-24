"""Student management endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.crud import student as student_crud
from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models import Driver
from app.schemas.student import StudentCreate, StudentOut

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Create a new student."""
    return student_crud.create_student(db, payload.name.strip(), payload.roll.strip(), payload.bus_id)


@router.get("", response_model=dict)
def list_students(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Get all students with pagination."""
    items, total = student_crud.get_students(db, page, page_size)
    return {
        "items": [StudentOut.model_validate(item).model_dump() for item in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Get a specific student by ID."""
    return student_crud.get_student_by_id(db, student_id)


@router.put("/{student_id}/assign/{bus_id}", response_model=StudentOut)
def assign_student(
    student_id: int,
    bus_id: int,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Assign a student to a bus."""
    return student_crud.assign_student_to_bus(db, student_id, bus_id)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    """Delete a student."""
    student_crud.delete_student(db, student_id)
