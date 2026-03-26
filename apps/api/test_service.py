from app.db.session import SessionLocal
from app.services.diamond_service import create_new_diamond, update_stage

db = SessionLocal()

# Create diamond
create_new_diamond(db, {
    "id": "D001",
    "stage": "procurement",
    "weight": 1.2,
    "value": 5000
})

print("✅ Diamond created")

# Move to cutting
update_stage(db, "D001", "cutting")

print("✅ Stage updated to cutting")