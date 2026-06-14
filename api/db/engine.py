from sqlalchemy import create_engine
from db.config import SQLITE_URL, POSTGRES_URL

def get_engine(mode: str):
    if mode == "local":
        return create_engine(
            SQLITE_URL,
            connect_args={"check_same_thread": False}  # sqlite only
        )

    return create_engine(POSTGRES_URL)
