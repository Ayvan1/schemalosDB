from pydantic import BaseModel
from datetime import datetime

class AlertData(BaseModel):
    time: datetime
    sensor_name: str 
    temperature: float
    