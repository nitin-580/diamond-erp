from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services.process_service import create_new_process, list_processes
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class ProcessCreate(BaseModel):
    name: str
    description: Optional[str] = None
    expected_duration: int # in minutes
    is_custom: Optional[bool] = True

class ProcessResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    expected_duration: int
    is_custom: bool

@router.post("/create", response_model=ProcessResponse)
def create(data: ProcessCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Check if admin
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create processes")
    
    return create_new_process(db, data.name, data.description, data.expected_duration, data.is_custom)

@router.get("/all", response_model=List[ProcessResponse])
def get_all(db: Session = Depends(get_db)):
    return list_processes(db)
