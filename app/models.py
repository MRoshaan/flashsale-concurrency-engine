# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "User"  # Matches your SQL table name
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    
    # Relationship to orders
    orders = relationship("Order", back_populates="owner")

class Product(Base):
    __tablename__ = "Product"  # Matches your SQL table name

    id = Column(Integer, primary_key=True, index=True)
    stock_quantity = Column(Integer, nullable=False)
    # Using the exact column name you created in SQL
    product_Name = Column(String(100)) 
    price = Column(Integer)

class Order(Base):
    __tablename__ = "Orders"  # Matches your SQL table name (Plural)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Product.id"), nullable=False)
    status = Column(String(20), default="PENDING") # PENDING, COMPLETED, FAILED
    
    # Relationships
    owner = relationship("User", back_populates="orders") 
