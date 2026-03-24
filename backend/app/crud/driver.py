"""CRUD operations for driver management."""

from sqlalchemy.orm import Session

from app.core.exceptions import InsufficientPermissionsException, ResourceNotFoundException
from app.models import Driver


def get_all_drivers(db: Session) -> list[Driver]:
    """Get all drivers."""
    return db.query(Driver).filter(Driver.role == "driver").order_by(Driver.id.asc()).all()


def get_driver_by_id(db: Session, driver_id: int) -> Driver:
    """Get a driver by ID."""
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise ResourceNotFoundException("Driver")
    return driver


def assign_driver_to_bus(db: Session, bus_id: int, driver_id: int) -> Driver:
    """Assign a driver to a bus."""
    from app.models import Bus

    bus = db.query(Bus).filter(Bus.id == bus_id).first()
    if not bus:
        raise ResourceNotFoundException("Bus")

    driver = get_driver_by_id(db, driver_id)

    if driver.role.lower() != "driver":
        raise ValueError("Only driver role can be assigned")

    current_bus_driver = db.query(Driver).filter(Driver.bus_id == bus_id, Driver.id != driver_id).first()
    if current_bus_driver:
        current_bus_driver.bus_id = None

    driver.bus_id = bus_id
    db.commit()
    db.refresh(driver)
    return driver


def unassign_driver_from_bus(db: Session, driver_id: int) -> Driver:
    """Remove driver from bus assignment."""
    driver = get_driver_by_id(db, driver_id)
    driver.bus_id = None
    db.commit()
    db.refresh(driver)
    return driver
