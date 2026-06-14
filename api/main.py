from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.engine import get_engine
from db.session import SessionLocal, Base
import uvicorn
import argparse
from routes import events


parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["local", "cloud"], default="local")
args = parser.parse_args()

engine = get_engine(args.mode)
SessionLocal.configure(bind=engine)
Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:8000"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(events.router)
@app.get("/")
def root():
    return {"status": "ok", "message": "API running"}


def start():
    print("Starting FastAPI application...")
    uvicorn.run(
        "main:app",   host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True,
    )


if __name__ == "__main__":
    start()
