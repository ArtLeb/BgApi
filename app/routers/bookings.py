from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import SessionLocal, get_db
from app.models.booking_m import BookingModel
from app.models.client_m import ClientModel  
from app.models.service_m import ServiceModel
from app.schemas.booking_s import BookingCreateS, BookingS, BookingUpdateS

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingS)
def create_booking(booking: BookingCreateS, db: Session = Depends(get_db)):
    # Проверка существования клиента
    client = db.query(ClientModel).get(booking.client_telegram_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Проверка существования сервиса
    service = db.query(ServiceModel).get(booking.service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    new_booking = BookingModel(**booking.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/", response_model=list[BookingS])
def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(BookingModel).offset(skip).limit(limit).all()


@router.put("/{booking_id}", response_model=BookingS)
def update_booking(
    booking_id: int,
    booking_data: BookingUpdateS,
    db: Session = Depends(get_db)
):
    # Находим бронирование
    booking = db.query(BookingModel).get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Проверяем клиента (если обновляется client_telegram_id)
    if booking_data.client_telegram_id:
        client = db.query(ClientModel).get(booking_data.client_telegram_id)
        if not client:
            raise HTTPException(status_code=404, detail="New client not found")
    
    # Проверяем сервис (если обновляется service_id)
    if booking_data.service_id:
        service = db.query(ServiceModel).get(booking_data.service_id)
        if not service:
            raise HTTPException(status_code=404, detail="New service not found")
    
    # Обновляем данные
    update_data = booking_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(booking, key, value)
    
    try:
        db.commit()
        db.refresh(booking)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Update error: {str(e)}")
    
    return booking

@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).get(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    try:
        db.delete(booking)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Delete error: {str(e)}")
    
    return

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()