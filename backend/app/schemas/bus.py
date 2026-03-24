from pydantic import BaseModel, Field


class BusCreate(BaseModel):
    number: str = Field(min_length=1, max_length=30)
    route_id: int


class BusOut(BaseModel):
    id: int
    number: str
    route_id: int

    model_config = {"from_attributes": True}


class BusListResponse(BaseModel):
    items: list[BusOut]
    total: int
