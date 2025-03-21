# kitecore/config_manager.py

import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

REQUIRED_VARS = ["KITE_DB_MODE"]

missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

KITE_DB_MODE = os.getenv("KITE_DB_MODE")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///kitecore_local.db")
