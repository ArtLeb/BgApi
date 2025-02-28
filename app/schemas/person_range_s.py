# app/schemas/person_range_s.py
from pydantic import BaseModel

class PersonRangeBaseS(BaseModel):
    category_id: int
    name: str
    min_persons: int
    max_persons: int

class PersonRangeCreateS(PersonRangeBaseS):
    pass

class PersonRangeUpdateS(BaseModel):
    category_id: int | None = None
    name: str | None = None
    min_persons: int | None = None
    max_persons: int | None = None

class PersonRangeS(PersonRangeBaseS):
    range_id: int
    
    class Config:
        from_attributes = True  