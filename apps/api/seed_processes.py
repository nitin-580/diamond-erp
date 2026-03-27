from app.db.session import SessionLocal
from app.repositories.process_repo import create_process, get_process_by_name

STAGES = [
    ("procurement", "Diamond acquired", 120),
    ("planning", "Analyzing diamond for best output", 240),
    ("laser_cutting", "Preliminary cutting with laser", 180),
    ("cutting", "Regular cutting process", 300),
    ("polishing", "Smoothing and shining", 480),
    ("grading", "Final quality check", 60),
    ("inventory", "Added to stock", 15),
    ("sold", "Sale complete", 5)
]

db = SessionLocal()

for name, desc, duration in STAGES:
    if not get_process_by_name(db, name):
        create_process(db, name, desc, duration, is_custom=False)
        print(f"✅ Seeded process: {name}")
    else:
        print(f"Skipped {name}")

db.close()
