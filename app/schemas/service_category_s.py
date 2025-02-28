

# app/schemas/service_category_s.py
from pydantic import BaseModel

class ServiceCategoryBaseS(BaseModel):
    name: str

class ServiceCategoryCreateS(ServiceCategoryBaseS):
    pass

class ServiceCategoryUpdateS(BaseModel):
    name: str | None = None

class ServiceCategoryS(ServiceCategoryBaseS):
    id: int
    class Config:
        from_attributes = True