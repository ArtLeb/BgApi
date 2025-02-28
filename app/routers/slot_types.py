# app/routers/slot_types.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.config.database import SessionLocal, get_db
from app.models.slot_type_m import SlotTypeModel
from app.schemas.slot_type_s import (
    SlotTypeCreateS,
    SlotTypeS,
    SlotTypeUpdateS
)

router = APIRouter(prefix="/slot-types", tags=["slot_types"])

@router.post("/", response_model=SlotTypeS, status_code=status.HTTP_201_CREATED)
def create_slot_type(slot_type: SlotTypeCreateS, db: Session = Depends(get_db)):
    try:
        # Проверка уникальности имени
        existing = db.query(SlotTypeModel).filter(
            SlotTypeModel.name == slot_type.name
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slot type with this name already exists"
            )
            
        new_slot = SlotTypeModel(**slot_type.model_dump())
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        return new_slot
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data integrity error"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/", response_model=list[SlotTypeS])
def read_slot_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(SlotTypeModel).offset(skip).limit(limit).all()

@router.get("/{slot_id}", response_model=SlotTypeS)
def read_slot_type(slot_id: int, db: Session = Depends(get_db)):
    slot = db.query(SlotTypeModel).get(slot_id)
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slot type not found"
        )
    return slot

@router.put("/{slot_id}", response_model=SlotTypeS)
def update_slot_type(
    slot_id: int,
    slot_data: SlotTypeUpdateS,
    db: Session = Depends(get_db)
):
    try:
        slot = db.query(SlotTypeModel).get(slot_id)
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Slot type not found"
            )

        update_data = slot_data.model_dump(exclude_unset=True)
        
        # Проверка уникальности имени при обновлении
        if "name" in update_data:
            existing = db.query(SlotTypeModel).filter(
                SlotTypeModel.name == update_data["name"],
                SlotTypeModel.id != slot_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Name already taken"
                )

        for key, value in update_data.items():
            setattr(slot, key, value)
            
        db.commit()
        db.refresh(slot)
        return slot
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot duration format invalid"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slot_type(slot_id: int, db: Session = Depends(get_db)):
    try:
        slot = db.query(SlotTypeModel).get(slot_id)
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Slot type not found"
            )
            
        db.delete(slot)
        db.commit()
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()