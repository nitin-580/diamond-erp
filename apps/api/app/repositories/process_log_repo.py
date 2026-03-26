from sqlalchemy.orm import Session
from app.models.process_log import ProcessLog

def create_process_log(db: Session, log_data: dict):
    log = ProcessLog(**log_data)
    db.add(log)
    db.commit()
    return log