from  fastapi import APIRouter
from  src.controller.influx import read_all_temperature,read_all_temperature_by_time,read_temperature_from_a_sensor,read_temperature_from_a_sensor_by_time



router = APIRouter()

@router.get("/all_temperature")
def get_all_temperature():
    return read_all_temperature()

@router.get("/temperature_time/{time}")
def get_temperature_by_time(time:str):
    return read_all_temperature_by_time(time=time)

@router.get("/temperature_sensor/{sensor_index}")
def  get_temperature_by_sensor_name(sensor_index:int):
    print(sensor_index)
    return read_temperature_from_a_sensor(sensor_index=sensor_index)

@router.get("/temperature_sensor_by_time/{sensor_index}/{time}")
def get_temperature_by_time_sensor_name(sensor_index:int,time:str):
    return  read_temperature_from_a_sensor_by_time(sensor_index=sensor_index, time=time)