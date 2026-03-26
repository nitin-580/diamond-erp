from app.db.session import engine
from sqlalchemy import text

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ DB Connected:", result.scalar())
    except Exception as e:
        print("❌ DB Connection Failed:", e)

if __name__ == "__main__":
    test_connection()