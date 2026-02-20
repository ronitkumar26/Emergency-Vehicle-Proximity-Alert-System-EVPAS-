from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


# Request body for updating location
class AmbulanceUpdate(BaseModel):
    vehicle_number: str
    latitude: float
    longitude: float
    speed: float


# Response schema
class AmbulanceResponse(BaseModel):
    id: UUID
    vehicle_number: str
    latitude: float | None
    longitude: float | None
    speed: float | None
    is_active: bool
    last_updated: datetime

    class Config:
        from_attributes = True