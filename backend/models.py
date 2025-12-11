from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from backend.database import Base

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    people_count = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)