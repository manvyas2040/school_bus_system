"""Database models for the application."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Driver(Base):
    """Driver model representing a school bus driver."""

    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="driver")
    bus_id: Mapped[int | None] = mapped_column(ForeignKey("buses.id"), nullable=True)

    bus: Mapped["Bus | None"] = relationship("Bus", back_populates="driver", uselist=False)


class Route(Base):
    """Route model representing a school bus route."""

    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    buses: Mapped[list["Bus"]] = relationship("Bus", back_populates="route")


class Bus(Base):
    """Bus model representing a school bus."""

    __tablename__ = "buses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"), nullable=False)

    route: Mapped["Route"] = relationship("Route", back_populates="buses")
    driver: Mapped["Driver | None"] = relationship("Driver", back_populates="bus", uselist=False)
    students: Mapped[list["Student"]] = relationship("Student", back_populates="bus")
    gps: Mapped["GPS | None"] = relationship("GPS", back_populates="bus", uselist=False)


class Student(Base):
    """Student model representing a school student."""

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    roll: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    bus_id: Mapped[int | None] = mapped_column(ForeignKey("buses.id"), nullable=True)

    bus: Mapped["Bus | None"] = relationship("Bus", back_populates="students")


class GPS(Base):
    """GPS model for real-time bus tracking."""

    __tablename__ = "gps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bus_id: Mapped[int] = mapped_column(ForeignKey("buses.id"), unique=True, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    bus: Mapped["Bus"] = relationship("Bus", back_populates="gps")


class Timetable(Base):
    """Timetable model for bus schedules."""

    __tablename__ = "timetables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"), nullable=False)
    bus_number: Mapped[str] = mapped_column(String(30), nullable=False)
    checkpoint: Mapped[str] = mapped_column(String(120), nullable=False)
    eta_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationship to Route
    route: Mapped["Route"] = relationship("Route")


__all__ = ["Driver", "Route", "Bus", "Student", "GPS", "Timetable"]
