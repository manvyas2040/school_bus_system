"""API router that includes all endpoints."""

from fastapi import APIRouter

from app.api.endpoints import auth, buses, drivers, gps, routes, students, timetable

# Create API router
api_router = APIRouter(prefix="/api")

# Include all endpoint routers
api_router.include_router(auth.router)
api_router.include_router(routes.router)
api_router.include_router(buses.router)
api_router.include_router(students.router)
api_router.include_router(drivers.router)
api_router.include_router(gps.router)
api_router.include_router(timetable.router)

__all__ = ["api_router"]
