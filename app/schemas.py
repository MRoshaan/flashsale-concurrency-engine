# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    # We use 'orm_mode' so Pydantic can read data from SQLAlchemy models
    class Config:
        orm_mode = True

# --- PRODUCT SCHEMAS ---
class ProductBase(BaseModel):
    # MUST match your SQL column name exactly
    product_Name: str 
    price: int
    stock_quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

# --- ORDER SCHEMAS ---
class OrderBase(BaseModel):
    product_id: int
    user_id: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    status: str
    
    # We can nest the User and Product info inside the Order response if we want
    # For now, let's keep it simple
    class Config:
        orm_mode = True
