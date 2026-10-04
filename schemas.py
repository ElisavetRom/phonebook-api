from pydantic import BaseModel, EmailStr
from typing import Optional


class ContactCreate(BaseModel):
    """Схема для создания контакта (POST)."""
    username: str
    email: EmailStr
    mobile: Optional[str] = ""
    home: Optional[str] = ""


class ContactUpdate(BaseModel):
    """Схема для обновления контакта (PUT)."""
    username: str
    email: EmailStr
    mobile: Optional[str] = ""
    home: Optional[str] = ""


class ContactOut(BaseModel):
    """Схема ответа — что отдаём клиенту."""
    id: int
    username: str
    email: str
    mobile: Optional[str] = ""
    home: Optional[str] = ""

    class Config:
        from_attributes = True