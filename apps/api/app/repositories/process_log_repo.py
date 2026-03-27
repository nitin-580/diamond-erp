from sqlalchemy.orm import Session
from app.models.process_log import ProcessLog
from app.models.diamond import Diamond
from sqlalchemy import func


def create_process_log(db: Session, log_data: dict):
    log = ProcessLog(**log_data)
    db.add(log)
    db.commit()
    return log

def get_logs_by_diamond(db, diamond_id: str):
    return db.query(ProcessLog)\
        .filter(ProcessLog.diamond_id == diamond_id)\
        .order_by(ProcessLog.timestamp)\
        .all()
from datetime import datetime, timedelta

def get_stuck_diamonds(db, minutes=60):
    threshold = datetime.utcnow() - timedelta(minutes=minutes)

    subquery = db.query(
        ProcessLog.diamond_id,
        func.max(ProcessLog.timestamp).label("last_update")
    ).group_by(ProcessLog.diamond_id).subquery()

    result = db.query(
        Diamond.id,
        Diamond.stage,
        subquery.c.last_update
    ).join(
        subquery,
        Diamond.id == subquery.c.diamond_id
    ).filter(
        subquery.c.last_update < threshold
    ).all()

    return [
        {
            "diamond_id": r.id,
            "stage": r.stage,
            "last_updated": r.last_update
        }
        for r in result
    ]

from collections import defaultdict

def get_stage_durations(db):
    logs = db.query(ProcessLog)\
        .order_by(ProcessLog.diamond_id, ProcessLog.timestamp)\
        .all()

    stage_times = defaultdict(list)
    prev_logs = {}

    for log in logs:
        d_id = log.diamond_id

        if d_id in prev_logs:
            prev = prev_logs[d_id]

            duration = (log.timestamp - prev.timestamp).total_seconds() / 60

            stage_times[prev.to_stage].append(duration)

        prev_logs[d_id] = log

    # calculate average
    result = {}
    for stage, durations in stage_times.items():
        result[stage] = round(sum(durations) / len(durations), 2)

    return result

def throughput_per_day(db):
    result = db.query(
        func.date(ProcessLog.timestamp),
        func.count(ProcessLog.diamond_id)
    ).group_by(func.date(ProcessLog.timestamp)).all()

    return {
        str(date): count
        for date, count in result
    }