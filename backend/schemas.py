from pydantic import BaseModel
from datetime import datetime

class DetectionOut(BaseModel):
    id: int
    filename: str
    people_count: int
    timestamp: datetime

    class Config:
        orm_mode = True