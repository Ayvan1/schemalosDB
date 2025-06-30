from  fastapi import APIRouter
from src.controller.oracle import read_all_temperature,read_alert,set_alert
from  src.model.temperatureData import TemperatureData
import json

router  = APIRouter()


@router.get("/allTemperature")
def get_all_temperature():
    return read_all_temperature()

@router.post("/setAlert")
def post_alert(alertData:TemperatureData):
    with open("../store_temperature.json","w") as f:
        print()
        json.dump(alertData.dict(),f)
    print(alertData)
    return set_alert(alertData)

@router.get("/getAlert")
def get_alert():
    return  read_alert()