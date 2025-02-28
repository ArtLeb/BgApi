# app/schemas/service.py
from typing import Optional
from pydantic import BaseModel

class ServiceBaseS(BaseModel):
    category_id: int
    description: Optional[str] = None
    person_based_pricing: Optional[bool] = None  # Разрешено None
    slot_type_id: Optional[int] = None           # Разрешено None
    available_quantity: int
    price_per_unit: float
    is_active: bool = True
    is_mandatory: bool = False
    name: str
    person_range_id: Optional[int] = None
class ServiceCreateS(ServiceBaseS):
    pass



class ServiceUpdateS(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    person_based_pricing: Optional[bool] = None
    slot_type_id: Optional[int] = None
    available_quantity: Optional[int] = None
    price_per_unit: Optional[float] = None
    is_active: Optional[bool] = None
    is_mandatory: Optional[bool] = None
    person_range_id: Optional[int] = None

class ServiceUpdate(ServiceBaseS):
    pass  

class ServiceS(ServiceBaseS):
    service_id: int
    class Config:
        from_attributes = True