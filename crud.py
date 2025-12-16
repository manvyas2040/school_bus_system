from sqlalchemy.orm import Session
import models , schemas
from auth import get_password_hashed , verify_password


def create_driver(db:Session,username:str,password:str):
    driver = models.Driver(username = username,hash_password= get_password_hashed(password))
    db.add(driver);db.commit();db.flush(driver)
    return driver

def authantic_driver(db:Session , username: str, password : str):
    driver= db.query(models.Driver).filter(models.Driver.username == username).first()
    if not driver :
        return None
    if not verify_password(password,driver.hashed_password):
        return None
    return driver

def create_route(db:Session , name:str):
    r = models.Route(name = name)
    db.add(r);db.commit();db.flush(r);return r

def create_bus(number : int , route_id : int, db: Session):
    b = models.Bus(number = number, route_id = route_id)
    db.add(b)
    db.commit()
    db.flush(b)
    
    gps = models.GPS(bus_id = b.id,latitude=0.0,longitude=0.0)
    db.add(gps)
    db.commit()
    db.flush(gps)
    return b

def add_student(db : Session ,student : schemas.StudentCreate):
    s = models.Student(name = student.name, roll = student.roll,bus_id = student.bus_id)
    db.add(s);db.commit();db.flush(s);return s

def updete_gps(db:Session , bus_id = int,lat = float , lng = float):
    gps = db.query(models.GPS).filter(models.GPS.bus_id == bus_id).first()
    if not gps:
        gps = models.GPS(bus_id = bus_id , latitude = lat , longitude = lng)
        db.add(gps)
    else:
        gps.latitude = lat ;gps.longitude = lng
        db.commit();db.flush(gps)
        return gps
