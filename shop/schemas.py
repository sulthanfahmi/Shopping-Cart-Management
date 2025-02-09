from pydantic import BaseModel,EmailStr, Field
from datetime import datetime 
from typing import Optional, ClassVar
from enum import Enum
from fastapi import Query

# For the table name user

class display(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

class Config:
     orm_mode = True

class usercreate(BaseModel):
    email : EmailStr
    password : str
    role : str 

class updateUser(usercreate):
     pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
     id : Optional[int]  = None
    

class user(BaseModel):
     email : EmailStr

class VerifyEmail(BaseModel):
     email : str
     otp: str
    
# For the Seller Products Table

class add_Products(BaseModel):
     Products_name : str
     category : str
     original_price : str
     new_price : str
     created_at : datetime

class products(BaseModel):
     id : int
     Products_name : str
     category : str
     original_price : str
     new_price : str
     created_at : datetime
     owner_id : int
     owner : display

# For the Customer Products Table

class Buy(BaseModel):
     category_products :str
     original_price : str
     new_price : str
     current_user : int
   

class Customer(BaseModel):
     Products_name : str
     
class Details_List(BaseModel):
     Products_name : str
     Details : Buy

class cart(BaseModel):
     id : int
     Products_name: str
     category_products :str
     original_price : str
     new_price : str
     current_user : int
     

class Review(BaseModel):
     description : str
     Rating : int

class review_call(BaseModel):
     id : int
     description : str
     Rating : int
     created_at : datetime
     owner_id : int

class update_review(BaseModel):
     description : str
     Rating : int







     

