from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.database import Base, engine

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="School Bus Tracking System",
    version="1.0.0",
    description="A comprehensive real-time school bus tracking and management system",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:5501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


# Health check endpoint
@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "school-bus-tracking"}

