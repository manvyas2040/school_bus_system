from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import require_role
from app.crud import get_drivers
from app.database import get_db
from app.models import Driver
from app.schemas.driver import DriverListResponse, DriverOut

router = APIRouter(tags=["drivers"])


@router.get("/drivers", response_model=DriverListResponse)
def list_drivers(
    db: Session = Depends(get_db),
    _: Driver = Depends(require_role("admin")),
):
    items = get_drivers(db)
    return {
        "items": [DriverOut.model_validate(item).model_dump() for item in items],
        "total": len(items),
    }
