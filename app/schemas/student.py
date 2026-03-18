from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    roll: str = Field(min_length=1, max_length=60)
    bus_id: int | None = None


class StudentOut(BaseModel):
    id: int
    name: str
    roll: str
    bus_id: int | None

    model_config = {"from_attributes": True}


class StudentAssignResponse(BaseModel):
    id: int
    bus_id: int
