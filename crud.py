from sqlalchemy.orm import Session
import models,schemas
from auth import get_password_hash,verify_password

def create_driver(db:Session,username : str,password:str):
    driver = models.Driver(username = username , hashed_password=get_password_hash(password))
    db.add(driver)
    db.commit()
    db.flush(driver)
    return driver
def authenticate_driver(db: Session , username : str, password : str):
    driver = db.query(models.Driver).filter(models.Driver.username == username).first()
    if not driver:
        return None
    if not verify_password(password,driver.hashed_password):
        return None
    return driver

def create_route(db: Session, name: str):
    clean_name = name.strip()

    existing_route = (
        db.query(models.Route).filter(models.Route.name.ilike(clean_name)).first()
    )
    if existing_route:
        return None

    route = models.Route(name=clean_name)
    db.add(route)
    db.commit()
    db.refresh(route)
    return route


def create_bus(db: Session, number: int, route_id: int):
    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not route:
        return None   # prevents FK crash

    bus = models.Bus(number=number, route_id=route_id)
    db.add(bus)
    db.commit()
    db.refresh(bus)

    gps = models.GPS(bus_id=bus.id)
    db.add(gps)
    db.commit()

    return bus

def add_student(db : Session, student : schemas.StudentCreate):
    s = models.Student(name = student.name, roll= student.roll,bus_id=student.bus_id)
    db.add(s)
    db.commit()
    db.flush(s)
    return s

def update_gps(db: Session, bus_id: int, lat: float, lng: float):
    gps = db.query(models.GPS).filter(models.GPS.bus_id == bus_id).first()
    if not gps:
        return None
    gps.latitude = lat
    gps.longitude = lng
    db.commit()
    db.refresh(gps)
    return gps
