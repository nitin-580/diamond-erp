from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.worker_repo import create_worker, get_all_workers
from app.schemas.worker import WorkerCreate, WorkerResponse

router = APIRouter()

@router.post("/create", response_model=WorkerResponse)
def create(data: WorkerCreate, db: Session = Depends(get_db)):
    return create_worker(db, data.dict())

@router.get("/all", response_model=list[WorkerResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_workers(db)
