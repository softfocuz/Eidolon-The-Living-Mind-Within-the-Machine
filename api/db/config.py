import os
from dotenv import load_dotenv

load_dotenv()

DB_MODE = os.getenv("DB_MODE", "local")

SQLITE_URL = os.getenv("SQLITE_URL", "sqlite:///app.db")

POSTGRES_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+psycopg2://user:pass@db.supabase.co:5432/postgres"
)
