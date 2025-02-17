from datetime import datetime, date
from typing import List, Optional, Any, Self
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator

class ContactBase(BaseModel):
    name: str = Field(min_length=2, max_length=25)
    surname: str = Field(min_length=2, max_length=25)
    email: EmailStr
    phone: str = Field(min_length=9, max_length=13)
    birthday: date
    additional_data: Optional[str] = Field(max_length=200)

    @field_validator('birthday')
    def validate_birthday(cls, value: Any) -> Self:
        if value > date.today():
            raise ValueError('Birthday cannot be in future')
        return value

class ContactResponse(ContactBase):
    id: int
    created_at: datetime | None
    updated_at: Optional[datetime] | None

    model_config = ConfigDict(from_attributes=True)

class ContactBirthdayRequest(BaseModel):
    days: int = Field(ge=0, le=366)
