from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from sbr_db import engine, Sessionlocal, Base, get_db
import models, schemas, crud, auth
from auth import create_access_token, decode_token

from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI(title="school bus management ")
Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/driver/login")

#  auth endpoint 
@app.post("/driver/signup",response_model=schemas.Driverout)
def Driver_signup(data :schemas.Drivercreate,db:Session=Depends(get_db)):
    existing = db.query(models.Driver).filter(models.Driver.username==data.username).first()
    if existing:
        raise HTTPException(status_code=404,detail="username taken")
    driver = crud.create_driver(db,username=data.username,password = data.password)
    return driver

@app.post("/driver/login",response_model=schemas.Token)
def driver_login(from_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    driver = crud.authantic_driver(db,from_data.username,from_data.password)
    if not driver:
        raise HTTPException(status_code=400,detail="incorrect credentials")
    access_token = create_access_token({"sub": driver.username},)
    return {"access_token":access_token,"token_type":"bearer"}

def get_corrent_driver(token : str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401,detail="invalid token")
    username = payload["sub"]
    driver = db.query(models.Driver).filter(models.Driver.username==username).first()
    if not driver:
        raise HTTPException(status_code=401,detail="driver not found")
    return driver

# routes / bus / student
@app.post("/routes",response_model=schemas.Routeout)
def create_route(r : schemas.Routecreate, db :Session=Depends(get_db)):
    
    return crud.create_route(db,r.name)

@app.post("/buses",response_model=schemas.Busout)
def create_bus(b: schemas.Buscreate, db: Session = Depends(get_db)):
    return crud.create_bus(b.number,b.route_id, db)


@app.post("/students",response_model=schemas.Studentout)
def create_student(s:schemas.StudentCreate,db:Session=Depends(get_db)):
    return crud.add_student(db,s)
# assign student to bus
@app.post("/students/{student_id}/assign/{bus_id}",response_model=schemas.Studentout)
def assign_students(student_id : int,bus_id : int,db:Session=Depends(get_db)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404,detail="student not found")
    bus = db.query(models.Bus).get(bus_id)
    if not bus:
        raise HTTPException(status_code=404,detail="bus not found")
    student.bus_id = bus_id
    db.commit();db.refresh(student)
    return student
# timetable 
@app.post("/timetable",response_model=schemas.Timetableout)
def add_stop(t : schemas.Timetablecreate,db :Session=Depends(get_db)):
    tt = models.Timetable(route_id = t.route_id,stop_name = t.stop_name,time=t.time)
    db.add(tt);db.commit();db.refresh(tt)
    return tt

@app.get("/timetable/{route_id}",response_model=List[schemas.Timetableout])
def get_timetable(route_id : int,db:Session=Depends(get_db)):
    return db.query(models.Timetable).filter(models.Timetable.route_id==route_id).all()

# GPS updete(driver must to own the bus  to updete its gps)
@app.post("/gps/{bus_id}",response_model=schemas.GPSout)
def updete_gps(bus_id : int,data : schemas.GPSupdete,current_driver:models.Driver=Depends(get_corrent_driver),db : Session=Depends(get_db)):
    if not current_driver.bus_id or current_driver.bus_id != bus_id:
        raise HTTPException(status_code=403,detail="not allowed to updete this bus")
    gps = crud.updete_gps(db,bus_id,data.lititude,data.longitude)
    return gps

# public get gps
@app.get("/gps/{bus_id}",response_model=schemas.GPSout)
def get_gps(bus_id : int,db:Session=Depends(get_db)):
    gps = db.query(models.GPS).filter(models.GPS.bus_id == bus_id).first()
    if not gps:
        raise HTTPException(status_code=404,detail="no gps data")
    return gps


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(
#         "main:app",      # file_name:FastAPI_object
#         host="127.0.0.1",
#         port=8000,
#         reload=True
#     )
