from pydantic import BaseModel

class WorkerCreate(BaseModel):
    id: str
    name: str

class WorkerResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True