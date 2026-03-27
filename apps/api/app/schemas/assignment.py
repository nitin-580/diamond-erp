from pydantic import BaseModel

class AssignmentCreate(BaseModel):
    diamond_id: str
    worker_id: str