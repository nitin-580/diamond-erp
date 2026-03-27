from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # admin / manager / worker
    worker_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)