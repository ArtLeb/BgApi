# app/routers/__init__.py
from .clients import router
from .bookings import router as bookings_router
from .services import router as services_router
from .service_categories import router as service_categories_router
from .slot_types import router as slot_types_router
from .person_ranges import router as person_ranges_router

__all__ = [
    "clients_router",
    "bookings_router",
    "services_router",
    "service_categories_router",
    "slot_types_router",
    "person_ranges_router"
]