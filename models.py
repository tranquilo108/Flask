import datetime

from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class User(UserCreate):
    id: int


class UserUpdate(UserCreate):
    pass


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float


class Product(ProductCreate):
    id: int


class ProductUpdate(ProductCreate):
    pass


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    date: Optional[datetime.datetime]
    status: Optional[bool] = False


class Order(OrderCreate):
    id: int


class OrderUpdate(OrderCreate):
    pass
