from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.diamond_service import create_new_diamond, update_stage
from app.repositories.diamond_repo import get_diamond
from app.repositories.diamond_repo import get_diamonds_by_stage
from app.repositories.diamond_repo import get_all_diamonds
from app.repositories.process_log_repo import get_logs_by_diamond
from app.schemas.process_log import ProcessLogResponse
from fastapi import HTTPException

from app.schemas.diamond import (
    DiamondCreate,
    DiamondUpdateStage,
    DiamondResponse
)

router = APIRouter()


@router.post("/create", response_model=DiamondResponse)
def create_diamond(data: DiamondCreate, db: Session = Depends(get_db)):
    return create_new_diamond(db, data.dict())


@router.post("/update-stage")
def update_diamond_stage(data: DiamondUpdateStage, db: Session = Depends(get_db)):
    return update_stage(db, data.diamond_id, data.new_stage)


@router.get("/all", response_model=list[DiamondResponse])
def get_all(db: Session = Depends(get_db)):
    diamonds = get_all_diamonds(db)

    if diamonds is None:
        return []

    return diamonds


@router.get("/stage/{stage}", response_model=list[DiamondResponse])
def get_by_stage(stage: str, db: Session = Depends(get_db)):
    return get_diamonds_by_stage(db, stage)


@router.get("/{diamond_id}", response_model=DiamondResponse)
def get_diamond_by_id(diamond_id: str, db: Session = Depends(get_db)):
    diamond = get_diamond(db, diamond_id)

    if not diamond:
        raise HTTPException(status_code=404, detail="Diamond not found")

    return diamond

@router.get("/{diamond_id}/status")
def get_diamond_status(diamond_id: str, db: Session = Depends(get_db)):
    diamond = get_diamond(db, diamond_id)
    if not diamond:
        raise HTTPException(status_code=404, detail="Diamond not found")
    
    from datetime import datetime, timezone
    from app.repositories.process_repo import get_process_by_name
    
    process = get_process_by_name(db, diamond.stage)
    
    expected_duration = process.expected_duration if process else 60 # Default 60 mins
    
    now = datetime.now(timezone.utc)
    # stage_started_at is in UTC
    time_spent = (now - diamond.stage_started_at).total_seconds() / 60
    
    is_delayed = time_spent > expected_duration
    
    return {
        "diamond_id": diamond.id,
        "current_stage": diamond.stage,
        "started_at": diamond.stage_started_at,
        "time_spent_minutes": round(time_spent, 2),
        "expected_duration_minutes": expected_duration,
        "is_delayed": is_delayed,
        "description": process.description if process else "No description available"
    }

@router.get("/{diamond_id}/logs", response_model=list[ProcessLogResponse])
def get_logs(diamond_id: str, db: Session = Depends(get_db)):
    return get_logs_by_diamond(db, diamond_id)