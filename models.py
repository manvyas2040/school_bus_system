from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sbr_db import Base
import datetime


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    buses = relationship("Bus", back_populates="route")
    timetables = relationship("Timetable", back_populates="route")


class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True, nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)

    route = relationship("Route", back_populates="buses")
    driver = relationship("Driver", back_populates="bus", uselist=False)
    students = relationship("Student", back_populates="bus")
    gps = relationship("GPS", back_populates="bus", uselist=False)


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bus_id = Column(Integer, ForeignKey("buses.id"))

    bus = relationship("Bus", back_populates="driver")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    roll = Column(String, unique=True)
    bus_id = Column(Integer, ForeignKey("buses.id"))

    bus = relationship("Bus", back_populates="students")


class Timetable(Base):
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    stop_name = Column(String, nullable=False)
    time = Column(String, nullable=False)

    route = relationship("Route", back_populates="timetables")


class GPS(Base):
    __tablename__ = "gps"

    id = Column(Integer, primary_key=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), unique=True)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    bus = relationship("Bus", back_populates="gps")
