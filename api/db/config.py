import os

DB_MODE = os.getenv("DB_MODE", "local")  

SQLITE_URL = "sqlite:///app.db"

# Supabase Postgres connection string
POSTGRES_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+psycopg2://user:pass@db.supabase.co:5432/postgres" # not done with setup yet
)
