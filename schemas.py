from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RouteCreate(BaseModel):
    name: str

class RouteOut(RouteCreate):
    id: int
    class Config:
        from_attributes = True

class BusCreate(BaseModel):
    number: int
    route_id: int

class BusOut(BusCreate):
    id: int
    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    name: str
    roll: str
    bus_id: Optional[int]

class StudentOut(StudentCreate):
    id: int
    class Config:
        from_attributes = True

class GPSUpdate(BaseModel):
    latitude: float
    longitude: float

class GPSOut(BaseModel):
    bus_id: int
    latitude: float
    longitude: float
    updated_at: datetime
    class Config:
        from_attributes = True
