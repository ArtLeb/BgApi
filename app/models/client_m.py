from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class ClientModel(Base):
    __tablename__ = 'clients'
    telegram_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    phone_number = Column(String(12), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    
    # Обратное отношение к BookingModel
    bookings = relationship("BookingModel", back_populates="client")