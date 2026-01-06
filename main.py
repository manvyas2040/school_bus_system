from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sbr_db import engine, SessionLocal, Base,get_db
import models, schemas, crud
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from auth import create_access_token,decode_token

app = FastAPI(title="School Bus Management")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/driver/login")
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"status": "running"}

@app.post("/driver/signup",response_model=schemas.DriverOut)
def driver_signup(data : schemas.DriverCreate,db:Session=Depends(get_db)):
    exitsting = db.query(models.Driver).filter(models.Driver.username ==data.username).first()
    if exitsting:
        raise HTTPException(status_code=400,detail="user name taken")
    driver = crud.create_driver(db,username=data.username,password=data.password)
    return driver

@app.post("/driver/login",response_model=schemas.Token)
def driver_login(from_data : OAuth2PasswordRequestForm=Depends(),db : Session=Depends(get_db)):
    driver = crud.authenticate_driver(db,from_data.username,from_data.password)
    if not driver:
        raise HTTPException(status_code=400,detail="incorrect credentils")
    acces_token = create_access_token({"sub":driver.username})
    return {"access_token" : acces_token,"token_type" : "bearer"}

def get_current_driver(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload["sub"]
    driver = db.query(models.Driver).filter(models.Driver.username==username).first()
    if not driver:
        raise HTTPException(status_code=401, detail="Driver not found")
    return driver

@app.post("/routes", response_model=schemas.RouteOut)
def create_route(r: schemas.RouteCreate, db: Session = Depends(get_db)):
    route = crud.create_route(db, r.name)
    if not route:
        raise HTTPException(
            status_code=400,
            detail="Route name already exists"
        )
    return route

@app.post("/buses", response_model=schemas.BusOut)
def create_bus(b: schemas.BusCreate, db: Session = Depends(get_db)):
    bus =crud.create_bus(db, b.number, b.route_id)
    if not bus:
        raise HTTPException(400, "Route does not exist")
    return bus

@app.post("/students", response_model=schemas.StudentOut)
def create_student(s: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.add_student(db, s)


@app.put("/students/{student_id}/assign/{bus_id}", response_model=schemas.StudentOut)
def assign_student(student_id: int, bus_id: int, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)
    bus = db.get(models.Bus, bus_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    bus = db.query(models.Bus).get(bus_id)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    student.bus_id = bus_id
    db.commit(); db.refresh(student)
    return student


@app.get("/gps/{bus_id}", response_model=schemas.GPSOut)
def get_gps(bus_id: int, db: Session = Depends(get_db)):
    gps = db.query(models.GPS).filter(models.GPS.bus_id==bus_id).first()
    if not gps:
        raise HTTPException(status_code=404, detail="No GPS data ")
    return gps

@app.post("/gps/{bus_id}", response_model=schemas.GPSOut)
def update_gps(bus_id: int, data: schemas.GPSUpdate, db: Session = Depends(get_db)):
    gps = crud.update_gps(db, bus_id, data.latitude, data.longitude)
    if not gps:
        raise HTTPException(404, "GPS not found")
    return gps  
