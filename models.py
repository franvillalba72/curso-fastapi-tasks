from pydantic import BaseModel, field_validator, Field, EmailStr, AnyUrl
from typing import Optional, List
from enum import Enum


class StatusType(str, Enum):
    DONE = "done"
    PENDING = "pending"


class MyBaseModel(BaseModel):
    id: int = Field(1, gt=0)

    # @field_validator('id')
    # def id_greater_than_zero(cls, value: int):
    #     if value > 0:
    #         return value
    #     raise ValueError('Must be greater than zero')


class Category(MyBaseModel):
    name: str


class User(MyBaseModel):
    name: str = Field(min_length=5)
    surname: str
    email: EmailStr
    website: AnyUrl


class Task(MyBaseModel):
    name: str = Field(min_length=5)
    description: Optional[str] = Field(None, min_length=5)
    status: StatusType
    category: Category
    user: User
    # tags: List[str] = []   # Para meter una lista como campo. Admite duplicados
    tags: set[str] = set()  # El set es una lista que no admite duplicados

    @field_validator('name')
    def name_alphanumeric(cls, value: str):
        if value.replace(' ', '').isalnum() and len(value.replace(' ', '')) > 0:
            return value
        raise ValueError('Must be alphanumeric and not blank')
