from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.diamond_service import create_new_diamond, update_stage
from app.repositories.diamond_repo import get_diamond

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


@router.get("/{diamond_id}", response_model=DiamondResponse)
def get_diamond_by_id(diamond_id: str, db: Session = Depends(get_db)):
    return get_diamond(db, diamond_id)

@router.get("/all", response_model=list[DiamondResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_diamonds(db)