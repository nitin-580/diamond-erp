from pydantic import BaseModel
from datetime import datetime

class ProcessLogResponse(BaseModel):
    diamond_id: str
    from_stage: str
    to_stage: str
    description: Optional[str] = None
    is_skipped: bool = False
    timestamp: datetime

    class Config:
        from_attributes = True