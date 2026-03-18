from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, buses, drivers, gps, routes, students, timetable

Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Bus Tracking System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:5501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(routes.router)
app.include_router(buses.router)
app.include_router(students.router)
app.include_router(gps.router)
app.include_router(timetable.router)
app.include_router(drivers.router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": "school-bus-tracking"}
