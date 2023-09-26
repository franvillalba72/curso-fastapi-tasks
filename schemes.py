from pydantic import BaseModel, field_validator, Field, EmailStr, AnyUrl
from typing import Optional, List
from enum import Enum


class StatusType(str, Enum):
    DONE = "done"
    PENDING = "pending"


class MyBaseModel(BaseModel):
    id: int = Field(1, gt=0, autoincrement=True, Optional=True)


class Category(MyBaseModel):
    name: str


class User(MyBaseModel):
    name: str = Field(min_length=5)
    surname: str
    email: EmailStr
    website: AnyUrl


class Task(MyBaseModel):
    name: str = Field(min_length=3)
    description: Optional[str] = Field(None, min_length=3)
    status: StatusType
    # category: Category
    # user: User
    category_id: int = Field(ge=1, le=1000)
    user_id: int = Field(ge=1)
    tags: set[str] = set()  # El set es una lista que no admite duplicados

    # Definimos unos datos de ejemplo para pruebas
    class Config:
        from_attributes = True

    @field_validator('name')
    def name_alphanumeric(cls, value: str):
        if value.replace(' ', '').isalnum() and len(value.replace(' ', '')) > 0:
            return value

        raise ValueError('Must be alphanumeric and not blank')
