from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

class BookingBaseS(BaseModel):
    service_id: int
    object_id: Optional[int] = Field(default=None)
    booking_date: datetime
    start_time: datetime
    end_time: datetime
    quantity: Optional[int] = Field(default=None)
    total_price: Optional[Decimal] = Field(default=None)
    is_paid: Optional[bool] = Field(default=None)  # Разрешено None
    is_confirmed: Optional[bool] = Field(default=None)  # Разрешено None

class BookingCreateS(BookingBaseS):
    client_telegram_id: Optional[int] = Field(default=None)  # Разрешено None
    added_to_cart_time: datetime

class BookingS(BookingBaseS):
    booking_id: int
    client_telegram_id: Optional[int] = Field(default=None)  # Разрешено None
    added_to_cart_time: datetime

class BookingUpdateS(BaseModel):
    service_id: Optional[int] = None
    object_id: Optional[int] = None
    booking_date: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    quantity: Optional[int] = None
    total_price: Optional[Decimal] = None
    is_paid: Optional[bool] = None
    is_confirmed: Optional[bool] = None
    client_telegram_id: Optional[int] = None
    added_to_cart_time: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


