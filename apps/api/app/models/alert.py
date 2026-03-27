from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
from app.db.base import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    worker_id = Column(String, nullable=True)
    diamond_id = Column(String, nullable=True)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)