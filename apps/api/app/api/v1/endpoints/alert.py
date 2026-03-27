from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.alert_repo import get_all_alerts
from app.api.deps import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/alerts")
def alerts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_all_alerts(db)