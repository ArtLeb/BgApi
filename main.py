from fastapi import Depends, FastAPI
from app.routers import  bookings, clients, person_ranges, services,  slot_types, service_categories
from app.config.database import SessionLocal, engine, get_db
#from app.routers.service_categories import ServiceCategoryS, ServiceCategoryCreateS

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Берег Бекэнд", version="1.0.0")

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clients.router)
app.include_router(bookings.router)
app.include_router(service_categories.router)
app.include_router(slot_types.router)
app.include_router(person_ranges.router)
app.include_router(services.router)



@app.get("/")
def root():
    return {"message": "BeregAPI - Система бронирования ресурсов для тестов"}