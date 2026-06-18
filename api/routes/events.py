from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime

import csv
import io

from db.session import get_db
from db.models import Event
from schemas.events import EventCreate, EventResponse

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    obj = Event(**event.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


@router.get("/", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return (
        db.query(Event)
        .filter(Event.is_deleted == False)
        .limit(100)
        .all()
    )


@router.get("/{session_id}", response_model=EventResponse)
def get_event(session_id: str, db: Session = Depends(get_db)):
    event = (
        db.query(Event)
        .filter(Event.session_id == session_id, Event.is_deleted == False)
        .first()
    )

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.delete("/{session_id}")
def delete_event(session_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.session_id == session_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.is_deleted = True
    db.commit()

    return {"status": "deleted"}



@router.post("/upload-csv")
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    BATCH_SIZE = 500

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))

    batch = []
    total_inserted = 0

    for row in reader:
        obj = Event(
            session_id=int(row["session_id"]),
            app_name=row["app_name"],
            app_category=row["app_category"],
            previous_app=None if row["previous_app"] == "None" else row["previous_app"],

            timestamp=datetime.strptime(
                row["timestamp"],
                "%Y-%m-%d %H:%M:%S"
            ),

            date=row["date"],
            hour_of_day=int(row["hour_of_day"]),
            day_of_week=row["day_of_week"],
            is_weekend=bool(int(row["is_weekend"])),

            session_duration_sec=int(row["session_duration_sec"]),
            session_duration_hms=row["session_duration_hms"],

            cpu_usage_pct=float(row["cpu_usage_pct"]),
            ram_usage_mb=float(row["ram_usage_mb"]),
            network_usage_mb=float(row["network_usage_mb"]),
            battery_drain_pct=float(row["battery_drain_pct"]),

            is_anomaly=bool(int(row["is_anomaly"])),

            session_duration_min=int(row["session_duration_min"]),
            day_part=str(row["day_part"]),
            session_duration_sec_outlier=bool(int(row["session_duration_sec_outlier"])),
            cpu_usage_pct_outlier=bool(int(row["cpu_usage_pct_outlier"])),
            ram_usage_mb_outlier=bool(int(row["ram_usage_mb_outlier"])),
            network_usage_mb_outlier=bool(int(row["network_usage_mb_outlier"])),
            battery_drain_pct_outlier=bool(int(row["battery_drain_pct_outlier"])),
            previous_to_current_probability=float(row["previous_to_current_probability"])
        )

        batch.append(obj)

        if len(batch) >= BATCH_SIZE:
            db.bulk_save_objects(batch)
            db.commit()
            total_inserted += len(batch)
            batch.clear()

    if batch:
        db.bulk_save_objects(batch)
        db.commit()
        total_inserted += len(batch)

    return {"inserted": total_inserted}
