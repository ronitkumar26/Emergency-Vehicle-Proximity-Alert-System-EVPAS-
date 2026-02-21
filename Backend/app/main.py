from fastapi import FastAPI
from app.database import engine, Base
from app.models import ambulance
from app.routes import ambulance, vehicles
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.simulator import simulate_ambulance_movement


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_simulator():
    asyncio.create_task(simulate_ambulance_movement())

    
@app.get("/")
def root():
    return {"message": "EVPAS Backend Running"}

app.include_router(ambulance.router)
app.include_router(vehicles.router)