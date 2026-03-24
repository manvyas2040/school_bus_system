from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.security import create_access_token, create_refresh_token, decode_token
from app.crud import authenticate_user, create_user
from app.database import get_db
from app.models import Driver
from app.schemas.auth import LoginResponse, MeResponse, RefreshRequest, SignupRequest, TokenPair

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=dict)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    user = create_user(db, payload.username.strip(), payload.password, payload.role)
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "bus_id": user.bus_id,
    }


@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(user.username, user.role)
    refresh_token = create_refresh_token(user.username, user.role)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username,
        "bus_id": user.bus_id,
    }


@router.post("/refresh", response_model=TokenPair)
def refresh_token(payload: RefreshRequest):
    try:
        decoded = decode_token(payload.refresh_token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    username = decoded.get("sub")
    role = decoded.get("role", "driver")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    return {
        "access_token": create_access_token(username, role),
        "refresh_token": create_refresh_token(username, role),
        "token_type": "bearer",
    }


@router.get("/me", response_model=MeResponse)
def me(current_user: Driver = Depends(get_current_user)):
    route_id = current_user.bus.route_id if current_user.bus else None
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "bus_id": current_user.bus_id,
        "route_id": route_id,
    }
