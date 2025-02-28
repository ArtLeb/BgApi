# app/routers/services.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import SessionLocal, get_db
from app.models.person_range_m import PersonRangeModel
from app.models.service_m import ServiceModel
from app.models.service_category_m import ServiceCategoryModel
from app.models.slot_type_m import SlotTypeModel
from app.schemas.person_range_s import PersonRangeS
from app.schemas.service_category_s import ServiceCategoryS
from app.schemas.service_s import   ServiceCreateS, ServiceUpdateS, ServiceS
from app.schemas.slot_type_s import SlotTypeS

router = APIRouter(prefix="/services", tags=["services"])

@router.post("/", response_model=ServiceS, status_code=status.HTTP_201_CREATED)
def create_service(service: ServiceCreateS, db: Session = Depends(get_db)):
    # Проверка существования связанных сущностей
    category = db.query(ServiceCategoryS).get(service.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Service category not found")
    
    slot_type = db.query(SlotTypeS).get(service.slot_type_id)
    if not slot_type:
        raise HTTPException(status_code=404, detail="Slot type not found")
    
    if service.person_range_id:
        person_range = db.query(PersonRangeS).get(service.person_range_id)
        if not person_range:
            raise HTTPException(status_code=404, detail="Person range not found")

    new_service = service(**service.dict())
    db.add(new_service)
    try:
        db.commit()
        db.refresh(new_service)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating service: {str(e)}"
        )
    return new_service

@router.get("/", response_model=List[ServiceS])
def read_services(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ServiceModel).offset(skip).limit(limit).all()

@router.get("/{service_id}", response_model=ServiceS)
def read_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(ServiceModel).get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.put("/{service_id}", response_model=ServiceS)
def update_service(
    service_id: int,
    service_data: ServiceUpdateS,
    db: Session = Depends(get_db)
):
    service = db.query(service).get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # Проверка обновляемых полей
    update_data = service_data.dict(exclude_unset=True)
    
    if "category_id" in update_data:
        category = db.query(ServiceCategoryS).get(update_data["category_id"])
        if not category:
            raise HTTPException(status_code=404, detail="New category not found")
    
    if "slot_type_id" in update_data:
        slot_type = db.query(SlotTypeS).get(update_data["slot_type_id"])
        if not slot_type:
            raise HTTPException(status_code=404, detail="New slot type not found")
    
    if "person_range_id" in update_data:
        person_range = db.query(PersonRangeS).get(update_data["person_range_id"])
        if not person_range:
            raise HTTPException(status_code=404, detail="New person range not found")

    for key, value in update_data.items():
        setattr(service, key, value)
    
    try:
        db.commit()
        db.refresh(service)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error updating service: {str(e)}"
        )
    return service

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(service).get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    try:
        db.delete(service)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error deleting service: {str(e)}"
        )
    return


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()