from sqlalchemy.orm import Session
import models

def create_route(db: Session, name: str):
    route = models.Route(name=name)
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

def update_gps(db: Session, bus_id: int, lat: float, lng: float):
    gps = db.query(models.GPS).filter(models.GPS.bus_id == bus_id).first()
    if not gps:
        return None
    gps.latitude = lat
    gps.longitude = lng
    db.commit()
    db.refresh(gps)
    return gps
