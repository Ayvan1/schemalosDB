from fastapi import FastAPI
from src.route.influx_route import  router
from src.route.oracle_route import router as rt
from fastapi.middleware.cors import CORSMiddleware
from src.controller.oracle import start_background_job
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(rt)


@app.on_event("startup")
def on_startup():
    with open("../store_temperature.json","r") as f:
        data = json.load(f)
    start_background_job(data["temperature"])

@app.get("/")
def read_root():
    return "Hello World"