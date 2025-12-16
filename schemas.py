from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime

class Routecreate(BaseModel):
    name : str

class Routeout(BaseModel):
    id : int
    name :str
    
    class config :
        orm_mode=True

class Buscreate(BaseModel):
    number : int
    route_id : int

class Busout(BaseModel):
    id :int
    rout_id : int
    number :int

    class config:
        orm_mode = True

class Drivercreate(BaseModel):
    username : str
    password : str

class Driverout(BaseModel):
    id : int
    username : str
    bus_id : Optional[int]
    
    class config:
        orm_mode = True

class StudentCreate(BaseModel):
    name : str
    roll : str
    bus_id : Optional[int]

class Studentout(BaseModel):
    id : int
    name : str
    bus_id : Optional[int]

    class config:
        orm_mode =True

class Timetablecreate(BaseModel):
    rout_id : int
    stop_name : str
    time : str

class Timetableout(BaseModel):
    id : int
    rout_id : int
    stop_name : str
    time : str

    class config:
        orm_mode = True

class GPSupdete(BaseModel):
    lititude : float
    longitude :float

class GPSout(BaseModel):
    bus_id : int
    lititude :float
    longitude : float
    updete_at  :datetime

    class config:
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_type : str

class Tokenplayload(BaseModel):
    username : str