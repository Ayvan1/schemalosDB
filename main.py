from fastapi import FastAPI
from src.route.influx_route import  router

app = FastAPI()


app.include_router(router)

@app.get("/")
def read_root():
    return "Hello World"
