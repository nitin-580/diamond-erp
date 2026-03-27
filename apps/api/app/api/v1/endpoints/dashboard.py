from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.diamond_repo import count_diamonds_by_stage
from app.repositories.assignment_repo import count_assignments_by_worker
from app.repositories.process_log_repo import get_stuck_diamonds
from app.repositories.process_log_repo import get_stage_durations




router = APIRouter()

@router.get("/stage-count")
def stage_count(db: Session = Depends(get_db)):
    return count_diamonds_by_stage(db)

@router.get("/worker-load")
def worker_load(db: Session = Depends(get_db)):
    return count_assignments_by_worker(db)

from app.repositories.assignment_repo import worker_performance

@router.get("/worker-performance")
def get_worker_performance(db: Session = Depends(get_db)):
    return worker_performance(db)


@router.get("/stuck-diamonds")
def stuck_diamonds(db: Session = Depends(get_db)):
    return get_stuck_diamonds(db)

@router.get("/stage-duration")
def stage_duration(db: Session = Depends(get_db)):
    return get_stage_durations(db)

from app.repositories.assignment_repo import worker_ranking

@router.get("/worker-ranking")
def get_worker_ranking(db: Session = Depends(get_db)):
    return worker_ranking(db)

from app.repositories.process_log_repo import throughput_per_day

@router.get("/throughput")
def throughput(db: Session = Depends(get_db)):
    return throughput_per_day(db)