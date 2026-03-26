from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class ProcessLog(Base):
    __tablename__ = "process_logs"

    id = Column(String, primary_key=True)
    diamond_id = Column(String)

    from_stage = Column(String)
    to_stage = Column(String)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())