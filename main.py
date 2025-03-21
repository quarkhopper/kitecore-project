from kitecore.config_manager import KITE_DB_MODE, DATABASE_URL
from lib.database import get_database, CloudDatabase
from lib.models import Base

print(f"Running in {KITE_DB_MODE} mode with DB: {DATABASE_URL}")

db = get_database()
db.connect()
print("Database connected successfully.")

if isinstance(db, CloudDatabase):
    try:
        print("Creating tables...")
        Base.metadata.create_all(db.get_engine())
        print("Tables created successfully.")
    except Exception as e:
        print(f"Failed to create tables: {e}")

db.close()
print("Database connection closed.")


