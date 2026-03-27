from sqlalchemy.orm import Session
from app.models.assignment import Assignment
from app.models.process_log import ProcessLog
from app.models.diamond import Diamond
from sqlalchemy import func
from sqlalchemy import Integer


import uuid

def create_assignment(db, diamond_id, worker_id):
    assignment = Assignment(
        id=str(uuid.uuid4()),
        diamond_id=diamond_id,
        worker_id=worker_id
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

def get_assignment_by_diamond(db, diamond_id):
    return db.query(Assignment)\
        .filter(Assignment.diamond_id == diamond_id)\
        .first()

def get_assignments_by_worker(db, worker_id):
    return db.query(Assignment)\
        .filter(Assignment.worker_id == worker_id)\
        .all()

def count_assignments_by_worker(db):
    result = db.query(
        Assignment.worker_id,
        func.count(Assignment.id)
    ).group_by(Assignment.worker_id).all()

    return {worker: count for worker, count in result}


def worker_performance(db):
    result = db.query(
        Diamond.current_worker_id,
        func.count(Diamond.id),
        func.sum(
            (Diamond.status == "completed").cast(Integer)
        ),
        func.sum(
            (Diamond.status == "in_progress").cast(Integer)
        )
    ).group_by(Diamond.current_worker_id).all()

    response = {}

    for worker_id, total, completed, in_progress in result:
        response[worker_id] = {
            "total": total,
            "completed": completed or 0,
            "in_progress": in_progress or 0
        }

    return response

def worker_ranking(db):
    result = db.query(
        Diamond.current_worker_id,
        func.count(Diamond.id).label("total"),
        func.sum(
            (Diamond.status == "completed").cast(Integer)
        ).label("completed"),
        func.sum(
            (Diamond.status == "in_progress").cast(Integer)
        ).label("in_progress")
    ).group_by(Diamond.current_worker_id).all()

    ranking = []

    for worker_id, total, completed, in_progress in result:
        ranking.append({
            "worker_id": worker_id,
            "completed": completed or 0,
            "in_progress": in_progress or 0,
            "score": completed or 0
        })

    # 🔥 sort by score
    ranking.sort(key=lambda x: x["score"], reverse=True)

    return ranking