from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.config.database import SessionLocal, get_db
from app.models.client_m import ClientModel
from app.schemas.client_s import (
    ClientCreateSchem,
    ClientSchem,
    ClientUpdateSchem
)

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientSchem, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreateSchem, db: Session = Depends(get_db)):
    try:
        existing = db.query(ClientModel).filter(
            (ClientModel.telegram_id == client.telegram_id) |
            (ClientModel.phone_number == client.phone_number)
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Такой клиент существует"
            )
            
        new_client = ClientModel(**client.model_dump())
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client
        
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

@router.get("/", response_model=list[ClientSchem])
def read_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(ClientModel).offset(skip).limit(limit).all()

@router.get("/{telegram_id}", response_model=ClientSchem)
def read_client(telegram_id: int, db: Session = Depends(get_db)):
    client = db.query(ClientModel).get(telegram_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не сущесвует"
        )
    return client

@router.put("/{telegram_id}", response_model=ClientSchem)
def update_client(
    telegram_id: int,
    client_data: ClientUpdateSchem,
    db: Session = Depends(get_db)
):
    try:
        client = db.query(ClientModel).get(telegram_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент не сущесвует"
            )

        update_data = client_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(client, key, value)
            
        db.commit()
        db.refresh(client)
        return client
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой номер уже есть"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/{telegram_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(telegram_id: int, db: Session = Depends(get_db)):
    try:
        client = db.query(ClientModel).get(telegram_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент не сущесвует"
            )
            
        db.delete(client)
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