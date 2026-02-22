import asyncio
from datetime import datetime
from app.database import SessionLocal
from app.models.ambulance import Ambulance

current_lng = 77.1900   # Start far left
direction = 1

LEFT_BOUND = 77.1900
RIGHT_BOUND = 77.2400   # Go much further right before U-turn

async def simulate_ambulance_movement():
    global current_lng, direction

    while True:
        db = SessionLocal()
        ambulance = db.query(Ambulance).first()

        if ambulance:
            ambulance.latitude = 28.6145  # fixed road

            # Move ambulance
            current_lng += 0.002 * direction

            # U-turn only after fully crossing area
            if current_lng >= RIGHT_BOUND:
                direction = -1
            elif current_lng <= LEFT_BOUND:
                direction = 1

            ambulance.longitude = current_lng
            ambulance.last_updated = datetime.utcnow()

            db.commit()
            print("🚑 Ambulance moved")

        db.close()
        await asyncio.sleep(3)  