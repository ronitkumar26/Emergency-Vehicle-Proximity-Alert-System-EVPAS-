from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.vehicles import Vehicle
from app.schemas.vehicles import VehicleUpdate, VehicleResponse

router = APIRouter(prefix="/vehicle", tags=["Vehicle"])


# Update or Create Vehicle Location
@router.post("/update-location", response_model=VehicleResponse)
def update_vehicle_location(data: VehicleUpdate, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_number == data.vehicle_number).first()

    if not vehicle:
        vehicle = Vehicle(
            vehicle_number=data.vehicle_number,
            latitude=data.latitude,
            longitude=data.longitude,
            is_active=True,
            last_updated=datetime.utcnow()
        )
        db.add(vehicle)
    else:
        vehicle.latitude = data.latitude
        vehicle.longitude = data.longitude
        vehicle.is_active = True
        vehicle.last_updated=datetime.utcnow()

    db.commit()
    db.refresh(vehicle)

    return vehicle


# Get All Active Vehicles
@router.get("/", response_model=list[VehicleResponse])
def get_active_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).filter(Vehicle.is_active == True).all()


# Get Single Vehicle
@router.get("/{vehicle_number}", response_model=VehicleResponse)
def get_vehicle(vehicle_number: str, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_number == vehicle_number).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle