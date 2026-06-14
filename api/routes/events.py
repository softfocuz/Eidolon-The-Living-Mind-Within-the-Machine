from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
    return db.query(Event).limit(100).all()


@router.get("/{session_id}", response_model=EventResponse)
def get_event(session_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.session_id == session_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event
