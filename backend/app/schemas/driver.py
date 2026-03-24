from pydantic import BaseModel


class DriverOut(BaseModel):
    id: int
    username: str
    role: str
    bus_id: int | None

    model_config = {"from_attributes": True}


class DriverListResponse(BaseModel):
    items: list[DriverOut]
    total: int
