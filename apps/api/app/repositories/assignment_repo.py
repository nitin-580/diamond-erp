from sqlalchemy.orm import Session
from app.models.assignment import Assignment

def create_assignment(db: Session, data: dict):
    assignment = Assignment(**data)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment