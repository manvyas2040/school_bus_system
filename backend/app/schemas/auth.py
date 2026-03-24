from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    role: str = Field(pattern="^(admin|driver)$")


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class LoginResponse(TokenPair):
    role: str
    username: str
    bus_id: int | None


class MeResponse(BaseModel):
    id: int
    username: str
    role: str
    bus_id: int | None
    route_id: int | None
