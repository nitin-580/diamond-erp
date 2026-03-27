from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services.incentive_service import (
    add_incentive,
    get_worker_incentives as service_get_worker_incentives,
    get_monthly_incentive as service_get_monthly_incentive,
    get_total_incentive as service_get_total_incentive
)
from app.schemas.incentive import IncentiveCreate, IncentiveResponse, TotalIncentiveResponse
from typing import List

router = APIRouter()

@router.post("/add", response_model=IncentiveResponse)
def add_manual_incentive(data: IncentiveCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Check if admin/manager
    if current_user.get("role") not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Only admins or managers can manually add incentives")
    
    return add_incentive(db, data.worker_id, data.diamond_id, data.amount)

@router.get("/worker/{worker_id}", response_model=List[IncentiveResponse])
def get_incentives(worker_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Workers can only view their own
    if current_user.get("role") == "worker" and current_user.get("sub") != worker_id: # Usually 'sub' is user_id
        # Wait, if 'sub' is user_id, need to check if user maps to this worker_id
        # User model has a worker_id field. Let's assume current_user is the payload from decode_token
        if current_user.get("worker_id") != worker_id:
             raise HTTPException(status_code=403, detail="You can only view your own records")
    
    # Manager/Admin can see all
    return service_get_worker_incentives(db, worker_id)

@router.get("/monthly/{worker_id}", response_model=List[IncentiveResponse])
def get_monthly(worker_id: str, month: int, year: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Access control
    if current_user.get("role") == "worker" and current_user.get("worker_id") != worker_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return service_get_monthly_incentive(db, worker_id, month, year)

@router.get("/total/{worker_id}")
def get_total(worker_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Access control
    if current_user.get("role") == "worker" and current_user.get("worker_id") != worker_id:
        raise HTTPException(status_code=403, detail="Access denied")

    total = service_get_total_incentive(db, worker_id)
    return {"worker_id": worker_id, "total_incentive": total}
