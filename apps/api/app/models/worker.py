from sqlalchemy import Column, String
from app.db.base import Base

class Worker(Base):
    __tablename__ = "workers"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)