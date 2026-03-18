from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import require_role
from app.crud import create_route, get_routes
from app.database import get_db
from app.models import Driver
from app.schemas.route import RouteCreate, RouteOut

router = APIRouter(tags=["routes"])


@router.post("/routes", response_model=RouteOut)
def create_route_endpoint(
    payload: RouteCreate,
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    return create_route(db, payload.name.strip())


@router.get("/routes", response_model=list[RouteOut])
def list_routes(db: Session = Depends(get_db)):
    return get_routes(db)
