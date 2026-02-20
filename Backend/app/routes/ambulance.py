from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas.ambulance import AmbulanceUpdate, AmbulanceResponse
from app.database import get_db
from app.models.ambulance import Ambulance

router = APIRouter(prefix="/ambulance", tags=["Ambulance"])


# Update or Create Ambulance Location
@router.post("/update-location", response_model=AmbulanceResponse)
def update_ambulance_location(data: AmbulanceUpdate, db: Session = Depends(get_db)):
    ambulance = db.query(Ambulance).filter(Ambulance.vehicle_number == data.vehicle_number).first()
    if not ambulance:
        ambulance = Ambulance(
            vehicle_number=data.vehicle_number,
            latitude=data.latitude,
            longitude=data.longitude,
            speed=data.speed,
            is_active=True,
            last_updated=datetime.utcnow()
        )
        db.add(ambulance)
    else:
        ambulance.latitude = data.latitude
        ambulance.longitude = data.longitude
        ambulance.speed = data.speed
        ambulance.is_active = True
        ambulance.last_updated = datetime.utcnow()

    db.commit()
    db.refresh(ambulance)

    return ambulance


#  Get All Active Ambulances
@router.get("/", response_model=list[AmbulanceResponse])
def get_active_ambulances(db: Session = Depends(get_db)):
    ambulances = db.query(Ambulance).filter(Ambulance.is_active == True).all()
    return ambulances


#  Get Single Ambulance by Vehicle Number
@router.get("/{vehicle_number}", response_model=AmbulanceResponse)
def get_ambulance(vehicle_number: str, db: Session = Depends(get_db)):
    ambulance = db.query(Ambulance).filter(Ambulance.vehicle_number == vehicle_number).first()

    if not ambulance:
        raise HTTPException(status_code=404, detail="Ambulance not found")

    return ambulance