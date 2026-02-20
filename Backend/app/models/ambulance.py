import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.database import Base


class Ambulance(Base):
    __tablename__ = "ambulances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_number = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)
    is_active = Column(Boolean, default=False)
    last_updated = Column(DateTime, default=datetime.utcnow)