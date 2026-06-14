from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EventBase(BaseModel):
    session_id: str
    app_name: str
    app_category: str
    previous_app: Optional[str] = None
    timestamp: int
    date: str
    hour_of_day: int
    day_of_week: int
    is_weekend: bool
    session_duration_sec: int
    session_duration_hms: str
    cpu_usage_pct: float
    ram_usage_mb: float
    network_usage_mb: float
    battery_drain_pct: float
    is_anomaly: bool

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
