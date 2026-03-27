from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import SessionLocal
from app.services.location_service import update_worker_location
from app.api.deps import get_current_user

router = APIRouter()


class LocationRequest(BaseModel):
    worker_id: str
    latitude: float
    longitude: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/location")
def send_location(data: LocationRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return update_worker_location(db, data.worker_id, data.latitude, data.longitude)