from sqlalchemy import Column, String, Integer, Float, Boolean
from db.session import Base

class Event(Base):
    __tablename__ = "events"

    session_id = Column(String, primary_key=True)
    app_name = Column(String)
    app_category = Column(String)
    previous_app = Column(String)
    timestamp = Column(Integer)
    date = Column(String)
    hour_of_day = Column(Integer)
    day_of_week = Column(Integer)
    is_weekend = Column(Boolean)
    session_duration_sec = Column(Integer)
    session_duration_hms = Column(String)
    cpu_usage_pct = Column(Float)
    ram_usage_mb = Column(Float)
    network_usage_mb = Column(Float)
    battery_drain_pct = Column(Float)
    is_anomaly = Column(Boolean)
