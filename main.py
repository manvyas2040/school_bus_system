from fastapi import FastAPI, Depends, HTTPException,websockets
from sqlalchemy.orm import Session
from sbr_db import engine, SessionLocal, Base,get_db
import models, schemas, crud

app = FastAPI(title="School Bus Management")

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"status": "running"}

@app.post("/routes", response_model=schemas.RouteOut)
def create_route(r: schemas.RouteCreate, db: Session = Depends(get_db)):
    return crud.create_route(db, r.name)

@app.post("/buses", response_model=schemas.BusOut)
def create_bus(b: schemas.BusCreate, db: Session = Depends(get_db)):
    bus =crud.create_bus(db, b.number, b.route_id)
    if not bus:
        raise HTTPException(400, "Route does not exist")
    return bus

@app.post("/gps/{bus_id}", response_model=schemas.GPSOut)
def update_gps(bus_id: int, data: schemas.GPSUpdate, db: Session = Depends(get_db)):
    gps = crud.update_gps(db, bus_id, data.latitude, data.longitude)
    if not gps:
        raise HTTPException(404, "GPS not found")
    return gps  
