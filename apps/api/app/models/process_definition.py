from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class ProcessDefinition(Base):
    __tablename__ = "process_definitions"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    
    # Expected time in minutes
    expected_duration = Column(Integer, default=60)
    
    is_custom = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
