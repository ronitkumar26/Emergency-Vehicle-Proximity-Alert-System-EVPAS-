from pydantic import BaseModel
from datetime import datetime


class VehicleUpdate(BaseModel):
    vehicle_number: str
    latitude: float
    longitude: float


class VehicleResponse(BaseModel):
    id: int
    vehicle_number: str
    latitude: float
    longitude: float
    is_active: bool
    last_updated: datetime

    class Config:
        from_attributes = True