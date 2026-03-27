from sqlalchemy.orm import Session
from app.repositories.incentive_repo import (
    create_incentive,
    get_worker_incentives as repo_get_worker_incentives,
    get_monthly_incentives_filtered,
    get_total_earnings
)

# Fixed incentive amount - can be moved to config or settings later
DEFAULT_INCENTIVE_AMOUNT = 100.0

def add_incentive(db: Session, worker_id: str, diamond_id: str, amount: float = None):
    # Use default amount if not provided
    if amount is None:
        amount = DEFAULT_INCENTIVE_AMOUNT
    
    return create_incentive(db, worker_id, diamond_id, amount)

def get_worker_incentives(db: Session, worker_id: str):
    return repo_get_worker_incentives(db, worker_id)

def get_monthly_incentive(db: Session, worker_id: str, month: int, year: int):
    return get_monthly_incentives_filtered(db, worker_id, month, year)

def get_total_incentive(db: Session, worker_id: str):
    return get_total_earnings(db, worker_id)
