from pydantic import BaseModel
from datetime import datetime

class Record(BaseModel):
    host: str
    sensor_name: str 
    time: datetime
    temperature: float
    