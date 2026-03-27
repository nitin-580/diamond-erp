from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IncentiveCreate(BaseModel):
    worker_id: str
    diamond_id: str
    amount: float

class IncentiveResponse(BaseModel):
    id: str
    worker_id: str
    diamond_id: str
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True

class TotalIncentiveResponse(BaseModel):
    worker_id: str
    total_amount: float
