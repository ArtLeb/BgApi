from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class ServiceCategoryModel(Base):
    __tablename__ = 'service_categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    
    # Обратное отношение к ServiceModel
    services = relationship("ServiceModel", back_populates="category")


