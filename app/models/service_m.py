from sqlalchemy import Column, Integer, ForeignKey, Boolean, Numeric, String, Text
from sqlalchemy.orm import relationship
from app.config.database import Base

class ServiceModel(Base):
    __tablename__ = "services"
    service_id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("service_categories.id"))
    description = Column(Text)
    person_based_pricing = Column(Boolean, default=False)
    slot_type_id = Column(Integer, ForeignKey("slot_types.id"), nullable=True)
    available_quantity = Column(Integer)
    price_per_unit = Column(Numeric(10, 2))
    is_active = Column(Boolean)
    is_mandatory = Column(Boolean)
    name = Column(String(255))
    person_range_id = Column(Integer, ForeignKey("person_ranges.range_id"), nullable=True)
    
    # Связи
    category = relationship("ServiceCategoryModel", back_populates="services", lazy="joined")
    slot_type = relationship("SlotTypeModel", back_populates="services")
    person_range = relationship("PersonRangeModel", back_populates="services")
    bookings = relationship("BookingModel", back_populates="service")