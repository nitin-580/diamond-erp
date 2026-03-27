from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.auth_service import register_user, login_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(email: str, password: str, role: str, db: Session = Depends(get_db)):
    return register_user(db, email, password, role)


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    return login_user(db, email, password)