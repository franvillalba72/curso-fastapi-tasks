# Description: Esquemas de datos para la API
from pydantic import BaseModel, field_validator, Field, EmailStr, AnyUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum


class StatusType(str, Enum):
    DONE = "done"
    PENDING = "pending"


class Category(BaseModel):
    name: str


class User(BaseModel):
    name: str = Field(min_length=5)
    surname: str
    email: EmailStr
    website: str

    class Config:
        # orm_mode = True
        from_attributes = True


class UserCreate(User):
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)


class UserDB(User):
    hashed_password: str


class AccessToken(BaseModel):
    user_id: int
    access_token: str
    expiration_date: datetime

    class Config:
        # orm_mode = True
        from_attributes = True


class Task(BaseModel):
    name: str = Field(min_length=3)
    description: Optional[str] = Field(None, min_length=3)
    status: StatusType
    category_id: int = Field(ge=1, le=1000)
    user_id: int = Field(ge=1)
    # tags: set[str] = set()  # El set es una lista que no admite duplicados

    # Configuración del esquema
    model_config = {
        'from_attributes': True,
        "json_schema_extra": {
            "example": {
                "name": "Task 1",
                "description": "Task 1 description",
                "status": "pending",
                "category_id": 1,
                "user_id": 1
            }
        }
    }

    @field_validator('name')
    def name_alphanumeric(cls, value: str):
        if value.replace(' ', '').isalnum() and len(value.replace(' ', '')) > 0:
            return value

        raise ValueError('Must be alphanumeric and not blank')


class TaskRead(Task):
    id: int


class TaskWrite(Task):
    id: Optional[int] = Field(None, ge=1)
    user_id: Optional[int] = Field(None, ge=1)
