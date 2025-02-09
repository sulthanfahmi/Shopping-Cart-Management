from sqlalchemy import Column, Integer, String, Boolean, func, ForeignKey, Enum, DateTime, Text ,UniqueConstraint,ForeignKeyConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship



class user(Base):
    __tablename__= "Admin"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)
    role = Column(String, nullable=False)
    otp = Column(String)
    



class product(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, nullable=False)
    Products_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    original_price = Column(String, nullable=False)
    new_price = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)
    product_image = Column(String, default="default.jpg")
    owner_id = Column(Integer, ForeignKey("Admin.id", ondelete="CASCADE"), nullable=False) 
    owner = relationship("user")  


class Add_To_Cart(Base):
    __tablename__ = "Customer"

    id = Column(Integer, primary_key=True, nullable=False)
    Products_name = Column(String, nullable=False)
    category_products = Column(String)
    original_price = Column(String)
    new_price = Column(String)
    current_user = Column(Integer,ForeignKey("Admin.id", ondelete="CASCADE"))


class Customer_Reviews(Base):

    __tablename__ = "Reviews"


    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String,nullable = False)
    Rating = Column(Integer,nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)
    owner_id = Column(Integer,ForeignKey("Admin.id", ondelete="CASCADE"))


   





   



