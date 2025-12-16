from sqlalchemy import Column, Integer, Float, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from sbr_db import Base
import datetime
#temp func
class Route(Base):
    __tablename__ ="route"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,unique=True,index=True)

    buses =relationship("Bus",back_populates="route")
    timetable = relationship("Timetable",back_populates="route")

class Bus(Base):
    __tablename__ = "buses"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, index=True)
    route_id = Column(Integer, ForeignKey("route.id"))

    route = relationship("Route", back_populates="buses")
    driver = relationship("Driver", back_populates="bus", uselist=False)
    students = relationship("Student", back_populates="bus")  
    gps = relationship("GPS", back_populates="bus", uselist=False)

class Driver(Base):
    __tablename__ = "driver"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,index=True)
    hashed_password = Column(String)
    bus_id = Column(Integer,ForeignKey("buses.id"))

    bus = relationship("Bus",back_populates="driver")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    roll = Column(String, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"))

    bus = relationship("Bus", back_populates="students") 


class Timetable(Base):
    __tablename__ = "timetables"
    id = Column(Integer,primary_key=True,index=True)
    route_id = Column(Integer,ForeignKey("route.id"))
    stop_name = Column(String)
    time = Column(String)

    route = relationship("Route",back_populates="timetable")

class GPS(Base):
    __tablename__ ="gps"
    id = Column(Integer,primary_key=True,index=True)
    bus_id = Column(Integer,ForeignKey("buses.id"),index=True)
    latitude = Column(Float,default=0.0)
    longitude = Column(Float,default=0.0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    bus = relationship("Bus",back_populates="gps")
    



