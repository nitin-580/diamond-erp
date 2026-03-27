from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.assignment_service import assign_diamond
from app.schemas.assignment import AssignmentCreate
from app.repositories.assignment_repo import get_assignment_by_diamond
from app.repositories.assignment_repo import get_assignments_by_worker


router = APIRouter()

@router.post("/assign")
def assign(data: AssignmentCreate, db: Session = Depends(get_db)):
    return assign_diamond(db, data.diamond_id, data.worker_id)


@router.get("/diamond/{diamond_id}")
def get_assignment(diamond_id: str, db: Session = Depends(get_db)):
    assignment = get_assignment_by_diamond(db, diamond_id)

    if not assignment:
        return {"message": "No assignment found"}

    return assignment

@router.get("/worker/{worker_id}")
def get_worker_assignments(worker_id: str, db: Session = Depends(get_db)):
    return get_assignments_by_worker(db, worker_id)