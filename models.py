from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sbr_db  import Base
import datetime

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    buses = relationship("Bus", back_populates="route")

class Bus(Base):
    __tablename__ = "buses"
    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)
    route_id = Column(Integer, ForeignKey("routes.id"))

    route = relationship("Route", back_populates="buses")
    driver = relationship("Driver", back_populates="bus", uselist=False)
    students = relationship("Student", back_populates="bus")
    gps = relationship("GPS", back_populates="bus", uselist=False)

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    bus_id = Column(Integer, ForeignKey("buses.id"))

    bus = relationship("Bus", back_populates="driver")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    roll = Column(String)
    bus_id = Column(Integer, ForeignKey("buses.id"))

    bus = relationship("Bus", back_populates="students")

class GPS(Base):
    __tablename__ = "gps"
    id = Column(Integer, primary_key=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), unique=True)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    bus = relationship("Bus", back_populates="gps")
