from fastapi import FastAPI
from src.route.influx_route import  router
from src.route.oracle_route import router as rt
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def read_root():
    return "Hello World"
