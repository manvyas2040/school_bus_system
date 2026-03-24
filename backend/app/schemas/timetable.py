from pydantic import BaseModel, Field


class TimetableEntry(BaseModel):
    bus_number: str
    checkpoint: str
    eta_minutes: int


class TimetableResponse(BaseModel):
    route_id: int
    route_name: str
    entries: list[TimetableEntry]


class TimetableCreate(BaseModel):
    route_id: int = Field(gt=0)
    bus_number: str = Field(min_length=1, max_length=30)
    checkpoint: str = Field(min_length=1, max_length=120)
    eta_minutes: int = Field(ge=0)


class TimetableOut(BaseModel):
    id: int
    route_id: int
    bus_number: str
    checkpoint: str
    eta_minutes: int

    model_config = {"from_attributes": True}
