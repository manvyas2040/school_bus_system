from pydantic import BaseModel


class TimetableEntry(BaseModel):
    bus_number: str
    checkpoint: str
    eta_minutes: int


class TimetableResponse(BaseModel):
    route_id: int
    route_name: str
    entries: list[TimetableEntry]
