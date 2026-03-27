from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.incentive import Incentive
import uuid

def create_incentive(db: Session, worker_id: str, diamond_id: str, amount: float):
    incentive = Incentive(
        id=str(uuid.uuid4()),
        worker_id=worker_id,
        diamond_id=diamond_id,
        amount=amount
    )
    db.add(incentive)
    db.commit()
    db.refresh(incentive)
    return incentive

def get_worker_incentives(db: Session, worker_id: str):
    return db.query(Incentive).filter(Incentive.worker_id == worker_id).order_by(Incentive.created_at.desc()).all()

def get_all_incentives(db: Session):
    return db.query(Incentive).all()

def get_monthly_incentives_filtered(db: Session, worker_id: str, month: int, year: int):
    return db.query(Incentive).filter(
        Incentive.worker_id == worker_id,
        extract('month', Incentive.created_at) == month,
        extract('year', Incentive.created_at) == year
    ).all()

def get_total_earnings(db: Session, worker_id: str):
    return db.query(func.sum(Incentive.amount)).filter(Incentive.worker_id == worker_id).scalar() or 0.0
