# app/routers/service_categories.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.config.database import SessionLocal, get_db
from app.models.service_category_m import ServiceCategoryModel
from app.schemas.service_category_s import (
    ServiceCategoryCreateS,
    ServiceCategoryS,
    ServiceCategoryUpdateS
)

router = APIRouter(prefix="/service-categories", tags=["service_categories"])

@router.post("/", response_model=ServiceCategoryS, status_code=status.HTTP_201_CREATED)
def create_category(category: ServiceCategoryCreateS, db: Session = Depends(get_db)):
    try:
        existing = db.query(ServiceCategoryModel).filter(
            ServiceCategoryModel.name == category.name
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
            
        new_category = ServiceCategoryModel(**category.model_dump())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
        
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

@router.get("/", response_model=list[ServiceCategoryS])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(ServiceCategoryModel).offset(skip).limit(limit).all()

@router.get("/{category_id}", response_model=ServiceCategoryS)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(ServiceCategoryModel).get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.put("/{category_id}", response_model=ServiceCategoryS)
def update_category(
    category_id: int,
    category_data: ServiceCategoryUpdateS,
    db: Session = Depends(get_db)
):
    try:
        category = db.query(ServiceCategoryModel).get(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        update_data = category_data.model_dump(exclude_unset=True)
        
        if "name" in update_data:
            existing = db.query(ServiceCategoryModel).filter(
                ServiceCategoryModel.name == update_data["name"],
                ServiceCategoryModel.id != category_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Name already taken"
                )

        for key, value in update_data.items():
            setattr(category, key, value)
            
        db.commit()
        db.refresh(category)
        return category
        
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

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category = db.query(ServiceCategoryModel).get(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
            
        db.delete(category)
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