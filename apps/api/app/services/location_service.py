import uuid
from datetime import datetime
from app.models.worker_location import WorkerLocation
from app.models.alert import Alert
from app.repositories.location_repo import save_location
from app.repositories.alert_repo import create_alert
from app.services.geo_service import is_inside_geofence


def update_worker_location(db, worker_id, lat, lng):
    location = WorkerLocation(
        id=str(uuid.uuid4()),
        worker_id=worker_id,
        latitude=lat,
        longitude=lng,
        timestamp=datetime.utcnow()
    )

    save_location(db, location)

    inside = is_inside_geofence(lat, lng)

    if not inside:
        alert = Alert(
            id=str(uuid.uuid4()),
            type="worker_outside",
            worker_id=worker_id,
            message="Worker left premises"
        )
        create_alert(db, alert)

        return {"status": "OUTSIDE", "alert": True}

    return {"status": "INSIDE", "alert": False}