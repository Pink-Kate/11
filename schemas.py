from pydantic import BaseModel, EmailStr, validator
from datetime import date, datetime
from typing import Optional

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_date: date
    additional_data: Optional[str] = None

    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if not v or not v.strip():
            raise ValueError('Ім\'я та прізвище не можуть бути порожніми')
        return v.strip()

    @validator('phone')
    def validate_phone(cls, v):
        if not v or not v.strip():
            raise ValueError('Номер телефону не може бути порожнім')
        return v.strip()

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birth_date: Optional[date] = None
    additional_data: Optional[str] = None

    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Ім\'я та прізвище не можуть бути порожніми')
        return v.strip() if v else v

    @validator('phone')
    def validate_phone(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Номер телефону не може бути порожнім')
        return v.strip() if v else v

class Contact(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True