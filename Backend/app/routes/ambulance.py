from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas.ambulance import AmbulanceUpdate, AmbulanceResponse
from app.database import get_db
from app.models.ambulance import Ambulance
from app.models.vehicles import Vehicle
from app.utils.distance import haversine_distance

router = APIRouter(prefix="/ambulance", tags=["Ambulance"])


# Update or Create Ambulance Location
@router.post("/update-location")
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

    vehicles = db.query(Vehicle).filter(Vehicle.is_active == True).all()

    vehicles_in_range = []

    for vehicle in vehicles:
        distance = haversine_distance(
            ambulance.latitude,
            ambulance.longitude,
            vehicle.latitude,
            vehicle.longitude
        )

        if distance <= 0.7:  # 300 meters radius
            vehicles_in_range.append({
                "vehicle_number": vehicle.vehicle_number,
                "distance_km": round(distance, 2)
            })

    return {
        "ambulance": ambulance.vehicle_number,
        "vehicles_alerted": vehicles_in_range
    }


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

# This is a manual check endpoint to see which vehicles are in range of a specific ambulance.

# @router.post("/{vehicle_number}/check-alert")
# def check_alert(vehicle_number: str, db: Session = Depends(get_db)):
#     ambulance = db.query(Ambulance).filter(Ambulance.vehicle_number == vehicle_number).first()

#     if not ambulance:
#         raise HTTPException(status_code=404, detail="Ambulance not found")

#     vehicles = db.query(Vehicle).filter(Vehicle.is_active == True).all()

#     vehicles_in_range = []

#     for vehicle in vehicles:
#         distance = haversine_distance(
#             ambulance.latitude,
#             ambulance.longitude,
#             vehicle.latitude,
#             vehicle.longitude
#         )

#         if distance <= 2:  # 2 km radius
#             vehicles_in_range.append({
#                 "vehicle_number": vehicle.vehicle_number,
#                 "distance_km": round(distance, 2)
#             })

#     return {
#         "ambulance": ambulance.vehicle_number,
#         "vehicles_in_range": vehicles_in_range
#     }