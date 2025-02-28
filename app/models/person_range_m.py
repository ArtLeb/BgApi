from sqlalchemy import Column, SmallInteger, String, Integer, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.orm import relationship
from app.config.database import Base

class PersonRangeModel(Base):
    __tablename__ = "person_ranges"
    range_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    min_persons = Column(SMALLINT(unsigned=True), nullable=False)
    max_persons = Column(SMALLINT(unsigned=True), nullable=False)
    category_id = Column(Integer, ForeignKey('service_categories.id'))
    
    # Обратное отношение к ServiceModel
    services = relationship("ServiceModel", back_populates="person_range")
