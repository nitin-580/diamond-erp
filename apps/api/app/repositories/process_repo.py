from sqlalchemy.orm import Session
from app.models.process_definition import ProcessDefinition
import uuid

def create_process(db: Session, name: str, description: str, expected_duration: int, is_custom: bool = True):
    process = ProcessDefinition(
        id=str(uuid.uuid4()),
        name=name,
        description=description,
        expected_duration=expected_duration,
        is_custom=is_custom
    )
    db.add(process)
    db.commit()
    db.refresh(process)
    return process

def get_process_by_name(db: Session, name: str):
    return db.query(ProcessDefinition).filter(ProcessDefinition.name == name).first()

def get_all_processes(db: Session):
    return db.query(ProcessDefinition).all()
