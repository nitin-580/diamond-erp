from app.models.worker_location import WorkerLocation

def save_location(db, location):
    db.add(location)
    db.commit()
    db.refresh(location)
    return location