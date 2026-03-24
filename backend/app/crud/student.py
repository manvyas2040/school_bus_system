"""CRUD operations for student management."""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.models import Bus, Student


def create_student(db: Session, name: str, roll: str, bus_id: int | None = None) -> Student:
    """Create a new student."""
    duplicate = db.query(Student).filter(func.lower(Student.roll) == roll.lower()).first()
    if duplicate:
        raise ValueError("Roll already exists")

    if bus_id is not None:
        bus_exists = db.query(Bus).filter(Bus.id == bus_id).first()
        if not bus_exists:
            raise ResourceNotFoundException("Bus")

    student = Student(name=name, roll=roll, bus_id=bus_id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_students(db: Session, page: int = 1, page_size: int = 10) -> tuple[list[Student], int]:
    """Get all students with pagination."""
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)
    query = db.query(Student)
    total = query.count()
    items = query.order_by(Student.id.asc()).offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def get_student_by_id(db: Session, student_id: int) -> Student:
    """Get a student by ID."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ResourceNotFoundException("Student")
    return student


def assign_student_to_bus(db: Session, student_id: int, bus_id: int) -> Student:
    """Assign a student to a bus."""
    student = get_student_by_id(db, student_id)

    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        raise ResourceNotFoundException("Bus")

    student.bus_id = bus_id
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student_id: int) -> Student:
    """Delete a student."""
    student = get_student_by_id(db, student_id)
    db.delete(student)
    db.commit()
    return student


def update_student(db: Session, student_id: int, name: str | None = None, roll: str | None = None) -> Student:
    """Update student information."""
    student = get_student_by_id(db, student_id)

    if name:
        student.name = name

    if roll:
        duplicate = (
            db.query(Student)
            .filter(func.lower(Student.roll) == roll.lower(), Student.id != student_id)
            .first()
        )
        if duplicate:
            raise ValueError("Roll already exists")
        student.roll = roll

    db.commit()
    db.refresh(student)
    return student
