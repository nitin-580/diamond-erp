from app.models.worker import Worker

def create_worker(db, data):
    worker = Worker(**data)
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker

def get_worker(db, worker_id):
    return db.query(Worker).filter(Worker.id == worker_id).first()

def get_all_workers(db):
    return db.query(Worker).all()