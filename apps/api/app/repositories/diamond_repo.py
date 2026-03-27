from sqlalchemy.orm import Session
from app.models.diamond import Diamond
from sqlalchemy import func


def create_diamond(db: Session, diamond_data: dict):
    diamond = Diamond(**diamond_data)
    db.add(diamond)
    db.commit()
    db.refresh(diamond)
    return diamond


def get_diamond(db: Session, diamond_id: str):
    return db.query(Diamond).filter(Diamond.id == diamond_id).first()


def update_diamond_stage(db: Session, diamond_id: str, new_stage: str):
    diamond = db.query(Diamond).filter(Diamond.id == diamond_id).first()
    if not diamond:
        return None

    diamond.stage = new_stage
    diamond.stage_started_at = func.now()
    db.commit()
    db.refresh(diamond)
    return diamond

def get_all_diamonds(db):
    return db.query(Diamond).all()

def get_diamonds_by_stage(db, stage: str):
    return db.query(Diamond).filter(Diamond.stage == stage).all()

def count_diamonds_by_stage(db):
    result = db.query(
        Diamond.stage,
        func.count(Diamond.id)
    ).group_by(Diamond.stage).all()

    return {stage: count for stage, count in result}