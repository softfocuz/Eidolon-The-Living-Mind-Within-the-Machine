from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class EventBase(BaseModel):
    session_id: int
    app_name: str
    app_category: str
    previous_app: Optional[str] = None
    timestamp: datetime
    date: Optional[date] = None
    hour_of_day: int
    day_of_week: str
    is_weekend: bool
    session_duration_sec: int
    session_duration_hms: str
    cpu_usage_pct: float
    ram_usage_mb: float
    network_usage_mb: float
    battery_drain_pct: float
    is_anomaly: bool

    session_duration_min: int
    day_part: str
    session_duration_sec_outlier: Optional[bool] = False
    cpu_usage_usage_pct_outlier: Optional[bool] = False
    ram_usage_mb_outlier: Optional[bool] = False
    network_usage_mb_outlier: Optional[bool] = False
    battery_drain_pct_outlier: Optional[bool] = False
    previous_to_current_probability: float



class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
