# app/schemas/__init__.py
from .client_s import ClientBaseSchem, ClientCreateSchem, ClientSchem
from .booking_s import BookingS, BookingBaseS, BookingCreateS, BaseModel, BookingUpdateS
from .service_s import  ServiceBaseS, ServiceCreateS, ServiceUpdateS, ServiceS
from .service_category_s import ServiceCategoryBaseS, ServiceCategoryCreateS, ServiceCategoryS
from .slot_type_s import SlotTypeBaseS, SlotTypeCreateS, SlotTypeS
from .person_range_s import PersonRangeBaseS, PersonRangeCreateS, PersonRangeS