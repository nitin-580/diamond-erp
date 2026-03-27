from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from app.db.base import Base

class Incentive(Base):
    __tablename__ = "incentives"

    id = Column(String, primary_key=True)
    worker_id = Column(String, ForeignKey("workers.id"), index=True)
    diamond_id = Column(String, ForeignKey("diamonds.id"))
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Ensure search by worker is fast
    __table_args__ = (
        Index("ix_incentives_worker_created", "worker_id", "created_at"),
    )
