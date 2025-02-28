# app/routers/person_ranges.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.config.database import SessionLocal, get_db
from app.models.person_range_m import PersonRangeModel
from app.models.service_category_m import ServiceCategoryModel
from app.schemas.person_range_s import (
    PersonRangeCreateS,
    PersonRangeS,
    PersonRangeUpdateS
)

router = APIRouter(prefix="/person-ranges", tags=["person_ranges"])

@router.post("/", response_model=PersonRangeS, status_code=status.HTTP_201_CREATED)
def create_person_range(
    person_range: PersonRangeCreateS, 
    db: Session = Depends(get_db)
):
    try:
        # Проверка существования категории
        category = db.query(ServiceCategoryModel).get(person_range.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found"
            )

        new_range = PersonRangeModel(**person_range.model_dump())
        db.add(new_range)
        db.commit()
        db.refresh(new_range)
        return new_range

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data or duplicate entry"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/", response_model=list[PersonRangeS])
def read_person_ranges(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(PersonRangeModel).offset(skip).limit(limit).all()

@router.get("/{range_id}", response_model=PersonRangeS)
def read_person_range(range_id: int, db: Session = Depends(get_db)):
    person_range = db.query(PersonRangeModel).get(range_id)  # Теперь используется только range_id
    if not person_range:
        raise HTTPException(status_code=404, detail="Person range not found")
    return person_range

@router.put("/{range_id}", response_model=PersonRangeS)
def update_person_range(
    range_id: int,
    person_range_data: PersonRangeUpdateS,
    db: Session = Depends(get_db)
):
    try:
        person_range = db.query(PersonRangeModel).get(range_id)
        if not person_range:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Person range not found"
            )

        # Проверка новой категории (если указана)
        if person_range_data.category_id:
            category = db.query(ServiceCategoryModel).get(person_range_data.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New category not found"
                )

        update_data = person_range_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(person_range, key, value)
            
        db.commit()
        db.refresh(person_range)
        return person_range

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data format"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/{range_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person_range(range_id: int, db: Session = Depends(get_db)):
    try:
        person_range = db.query(PersonRangeModel).get(range_id)
        if not person_range:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Person range not found"
            )
            
        db.delete(person_range)
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