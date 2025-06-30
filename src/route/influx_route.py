from  fastapi import APIRouter
from  src.controller.influx import read_all_temperature, create_task, get_alert
from src.model.temperatureData import  TemperatureData


router = APIRouter()

@router.get("/all_temperature")
def get_all_temperature():
    return read_all_temperature()

@router.post("/set_alert")
def  post_alert(limit_temperature:TemperatureData):
    return create_task(limit_temperature=limit_temperature.temperature)

@router.get("/get_alert")
def get_alert_temperature():
    return get_alert()