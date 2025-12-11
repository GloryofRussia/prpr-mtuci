import os
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.database import Base, engine, SessionLocal
from backend.errors import validation_exception_handler, general_exception_handler
from backend.ml.detector import count_people
from backend.models import Detection

app = FastAPI()
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Paths are resolved relative to this file so uvicorn can be run from project root.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Serve static assets
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def root():
    return FileResponse(os.path.join(STATIC_DIR, "panel.html"))


@app.post("/analyze")
def analyze_video(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(filepath, "wb") as f:
            f.write(file.file.read())
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save file")

    try:
        people = count_people(filepath)
    except Exception:
        raise HTTPException(status_code=500, detail="YOLO processing error")

    db = SessionLocal()
    rec = Detection(filename=filename, people_count=people)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    db.close()

    return {"filename": filename, "people_count": people}


@app.get("/history")
def get_history():
    db = SessionLocal()
    items = db.query(Detection).all()
    db.close()
    return items