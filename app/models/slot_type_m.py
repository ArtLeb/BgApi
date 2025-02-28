from sqlalchemy import Column, Integer, String, Time
from app.config.database import Base
from sqlalchemy.orm import relationship

class SlotTypeModel(Base):
    __tablename__ = 'slot_types'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    slot_duration = Column(Time, nullable=False)


    services = relationship("ServiceModel", back_populates="slot_type")  


