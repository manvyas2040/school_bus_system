from datetime import datetime

from pydantic import BaseModel, Field


class GPSUpdate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class GPSOut(BaseModel):
    bus_id: int
    latitude: float
    longitude: float
    updated_at: datetime

    model_config = {"from_attributes": True}
