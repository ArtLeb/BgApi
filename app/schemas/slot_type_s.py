# app/schemas/slot_type_s.py
from pydantic import BaseModel
from datetime import time

class SlotTypeBaseS(BaseModel):
    name: str
    slot_duration: time

class SlotTypeCreateS(SlotTypeBaseS):
    pass

class SlotTypeUpdateS(BaseModel):
    name: str | None = None
    slot_duration: time | None = None

class SlotTypeS(SlotTypeBaseS):
    id: int
    class Config:
        from_attributes = True  # Замена orm_mode для Pydantic v2+