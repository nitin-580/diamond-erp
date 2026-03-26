from pydantic import BaseModel
from typing import Optional


class DiamondCreate(BaseModel):
    id: str
    stage: str
    weight: float
    value: float
    parent_id: Optional[str] = None


class DiamondUpdateStage(BaseModel):
    diamond_id: str
    new_stage: str


class DiamondResponse(BaseModel):
    id: str
    stage: str
    weight: float
    value: float
    status: str

    class Config:
        from_attributes = True