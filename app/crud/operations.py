from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth.security import hash_password, verify_password
from app.models import Bus, Driver, GPS, Route, Student


def create_user(db: Session, username: str, password: str, role: str) -> Driver:
    existing = db.query(Driver).filter(func.lower(Driver.username) == username.lower()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    user = Driver(username=username, hashed_password=hash_password(password), role=role.lower())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> Driver | None:
    user = db.query(Driver).filter(Driver.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_route(db: Session, name: str) -> Route:
    existing = db.query(Route).filter(func.lower(Route.name) == name.lower()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Route already exists")

    route = Route(name=name)
    db.add(route)
    db.commit()
    db.refresh(route)
    return route


def get_routes(db: Session) -> list[Route]:
    return db.query(Route).order_by(Route.id.asc()).all()


def create_bus(db: Session, number: str, route_id: int) -> Bus:
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")

    duplicate = db.query(Bus).filter(func.lower(Bus.number) == number.lower()).first()
    if duplicate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bus number already exists")

    bus = Bus(number=number, route_id=route_id)
    db.add(bus)
    db.flush()

    gps = GPS(bus_id=bus.id, latitude=0.0, longitude=0.0, updated_at=datetime.now(timezone.utc))
    db.add(gps)
    db.commit()
    db.refresh(bus)
    return bus


def get_buses(db: Session, search: str | None = None) -> list[Bus]:
    query = db.query(Bus)
    if search:
        query = query.filter(func.lower(Bus.number).contains(search.lower()))
    return query.order_by(Bus.id.asc()).all()


def get_drivers(db: Session) -> list[Driver]:
    return db.query(Driver).filter(Driver.role == "driver").order_by(Driver.id.asc()).all()


def assign_driver_to_bus(db: Session, bus_id: int, driver_id: int) -> Driver:
    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus not found")

    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")

    if driver.role.lower() != "driver":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only driver role can be assigned")

    current_bus_driver = db.query(Driver).filter(Driver.bus_id == bus_id, Driver.id != driver_id).first()
    if current_bus_driver:
        current_bus_driver.bus_id = None

    driver.bus_id = bus_id
    db.commit()
    db.refresh(driver)
    return driver


def create_student(db: Session, name: str, roll: str, bus_id: int | None) -> Student:
    duplicate = db.query(Student).filter(func.lower(Student.roll) == roll.lower()).first()
    if duplicate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Roll already exists")

    if bus_id is not None:
        bus_exists = db.query(Bus).filter(Bus.id == bus_id).first()
        if not bus_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus not found")

    student = Student(name=name, roll=roll, bus_id=bus_id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_students(db: Session, page: int = 1, page_size: int = 10) -> tuple[list[Student], int]:
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)
    query = db.query(Student)
    total = query.count()
    items = query.order_by(Student.id.asc()).offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def assign_student_to_bus(db: Session, student_id: int, bus_id: int) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus not found")

    student.bus_id = bus_id
    db.commit()
    db.refresh(student)
    return student


def update_bus_gps(db: Session, user: Driver, bus_id: int, latitude: float, longitude: float) -> GPS:
    if user.role.lower() != "driver":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only drivers can update GPS")
    if user.bus_id != bus_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Driver not assigned to this bus")

    gps = db.query(GPS).filter(GPS.bus_id == bus_id).first()
    if not gps:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GPS record not found")

    gps.latitude = latitude
    gps.longitude = longitude
    gps.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(gps)
    return gps


def get_bus_gps(db: Session, bus_id: int) -> GPS:
    gps = db.query(GPS).filter(GPS.bus_id == bus_id).first()
    if not gps:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GPS not found")
    return gps


def get_timetable_for_route(db: Session, route_id: int) -> dict:
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")

    buses = db.query(Bus).filter(Bus.route_id == route_id).order_by(Bus.id.asc()).all()
    checkpoints = ["Depot", "School Gate", "North Stop", "South Stop"]

    entries: list[dict] = []
    for idx, bus in enumerate(buses):
        entries.append(
            {
                "bus_number": bus.number,
                "checkpoint": checkpoints[idx % len(checkpoints)],
                "eta_minutes": 5 + (idx * 7),
            }
        )

    return {
        "route_id": route.id,
        "route_name": route.name,
        "entries": entries,
    }
