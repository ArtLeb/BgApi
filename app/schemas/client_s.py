from pydantic import BaseModel

class ClientBaseSchem(BaseModel):
    phone_number: str
    full_name: str

class ClientCreateSchem(ClientBaseSchem):
    telegram_id: int

class ClientUpdateSchem(BaseModel):
    phone_number: str | None = None
    full_name: str | None = None

class ClientSchem(ClientCreateSchem):
    class Config:
        from_attributes = True