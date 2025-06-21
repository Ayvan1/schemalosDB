from  fastapi import APIRouter
from src.controller.oracle import read_all_temperature,read_all_temperature_by_time,read_temperature_from_a_sensor,read_temperature_from_a_sensor_by_time


router  = APIRouter()



@router.get("/allTemperatur")
def get_all_temperature():
    return read_all_temperature()

@router.get("/temperatureTime/{time}")
def get_temperature_by_time(time:str):
    print(time)
    return read_all_temperature_by_time(time=time) 

@router.get("/temperatureSensor/{sensor_index}")
def  get_temperature_by_sensor_name(sensor_index:int):
    print(sensor_index)
    return read_temperature_from_a_sensor(sensor_index=sensor_index)

@router.get("/temperatureSensorByTime/{sensor_index}/{time}")
def get_temperature_by_time_sensor_name(sensor_index:int,time:str):
    return  read_temperature_from_a_sensor_by_time(sensor_index=sensor_index, time=time)
