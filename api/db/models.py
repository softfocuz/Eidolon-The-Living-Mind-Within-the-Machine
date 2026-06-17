import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Date, func
from api.db.session import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True)
    session_id = Column(Integer)
    app_name = Column(String)
    app_category = Column(String)
    previous_app = Column(String)
    timestamp = Column(DateTime, nullable=False)
    date = Column(Date)
    hour_of_day = Column(Integer)
    day_of_week = Column(String)
    is_weekend = Column(Boolean, default=False)
    session_duration_sec = Column(Integer)
    session_duration_hms = Column(String)
    cpu_usage_pct = Column(Float)
    ram_usage_mb = Column(Float)
    network_usage_mb = Column(Float)
    battery_drain_pct = Column(Float)
    is_anomaly = Column(Boolean, default=False)

    session_duration_min = Column(Integer)
    day_part = Column(String)
    session_duration_sec_outlier = Column(Boolean, default=False)
    cpu_usage_pct_outlier = Column(Boolean, default=False)
    ram_usage_mb_outlier = Column(Boolean, default=False)
    network_usage_mb_outlier = Column(Boolean, default=False)
    battery_drain_pct_outlier = Column(Boolean, default=False)
    previous_to_current_probability = Column(Float)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
