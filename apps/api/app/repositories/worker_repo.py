from sqlalchemy.orm import Session
from app.models.worker import Worker

def get_worker(db: Session, worker_id: str):
    return db.query(Worker).filter(Worker.id == worker_id).first()