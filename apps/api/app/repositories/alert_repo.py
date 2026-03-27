from app.models.alert import Alert

def create_alert(db, alert):
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def get_all_alerts(db):
    return db.query(Alert).all()