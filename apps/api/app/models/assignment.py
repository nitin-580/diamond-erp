from sqlalchemy import Column, String, ForeignKey
from app.db.base import Base

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(String, primary_key=True)
    diamond_id = Column(String, ForeignKey("diamonds.id"))
    worker_id = Column(String, ForeignKey("workers.id"))

    status = Column(String, default="assigned")