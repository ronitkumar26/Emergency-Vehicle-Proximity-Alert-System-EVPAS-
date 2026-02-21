import asyncio
from datetime import datetime
from app.database import SessionLocal
from app.models.ambulance import Ambulance

current_lng = 77.2000   # starting longitude
direction = 1           # 1 = move right, -1 = move left

async def simulate_ambulance_movement():
    global current_lng, direction

    while True:
        db = SessionLocal()
        ambulance = db.query(Ambulance).first()

        if ambulance:
            # Fixed latitude (straight horizontal road)
            ambulance.latitude = 28.6145

            # Move longitude left & right
            current_lng += 0.001 * direction

            # Reverse direction when reaching boundary
            if current_lng > 77.2200:
                direction = -1
            elif current_lng < 77.2000:
                direction = 1

            ambulance.longitude = current_lng
            ambulance.last_updated = datetime.utcnow()

            db.commit()
            print("🚑 Ambulance moved")

        db.close()
        await asyncio.sleep(3)