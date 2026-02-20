from fastapi import FastAPI
from app.database import engine, Base
from app.models import ambulance
from app.routes import ambulance 

app = FastAPI()

@app.get("/")
def root():
    return {"message": "EVPAS Backend Running"}

app.include_router(ambulance.router)