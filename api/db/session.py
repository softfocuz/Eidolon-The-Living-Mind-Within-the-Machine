from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
