from sqlalchemy.orm import Session
from app.models.diamond import Diamond

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
    db.commit()
    db.refresh(diamond)
    return diamond
    
def get_all_diamonds(db):
    return db.query(Diamond).all()