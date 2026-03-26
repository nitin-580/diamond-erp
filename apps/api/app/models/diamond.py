from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Diamond(Base):
    __tablename__ = "diamonds"

    id = Column(String, primary_key=True, index=True)
    parent_id = Column(String, ForeignKey("diamonds.id"), nullable=True)

    stage = Column(String, index=True)
    weight = Column(Float)
    value = Column(Float)

    status = Column(String, default="in_progress")
    current_worker_id = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())