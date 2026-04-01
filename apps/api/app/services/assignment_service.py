from app.repositories.diamond_repo import get_diamond
from app.repositories.worker_repo import get_worker
from app.repositories.assignment_repo import create_assignment

def assign_diamond(db, diamond_id, worker_id):
    diamond = get_diamond(db, diamond_id)
    if not diamond:
        raise Exception("Diamond not found")

    worker = get_worker(db, worker_id)
    if not worker:
        raise Exception("Worker not found")

    # 3. Update diamond with current worker
    diamond.current_worker_id = worker_id
    db.commit()

    return create_assignment(db, diamond_id, worker_id)