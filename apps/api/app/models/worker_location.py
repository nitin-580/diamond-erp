from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime
from app.db.base import Base

class WorkerLocation(Base):
    __tablename__ = "worker_locations"

    id = Column(String, primary_key=True, index=True)
    worker_id = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)