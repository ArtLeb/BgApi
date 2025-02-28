from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, TIMESTAMP, SmallInteger, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class BookingModel(Base):
    __tablename__ = 'bookings'
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    client_telegram_id = Column(BigInteger, ForeignKey('clients.telegram_id', onupdate="CASCADE", ondelete="CASCADE"))
    service_id = Column(Integer, ForeignKey('services.service_id', onupdate="CASCADE", ondelete="CASCADE"))
    object_id = Column(Integer, nullable=True)
    added_to_cart_time = Column(TIMESTAMP, default=datetime.utcnow)  # Исправлено!
    booking_date = Column(TIMESTAMP)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    quantity = Column(SmallInteger, nullable=True)
    total_price = Column(DECIMAL(10,2), nullable=True)
    is_paid = Column(Boolean, default=False)
    is_confirmed = Column(Boolean, default=False)
    
    # Связи
    client = relationship("ClientModel", back_populates="bookings")
    service = relationship("ServiceModel", back_populates="bookings")

    