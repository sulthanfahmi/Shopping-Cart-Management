from typing import Optional, List
from fastapi import  FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session 
from .import models
from .database import engine,get_db
from .routers import Customer, Seller, user,admin,review


models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host = "localhost" ,database = "Shopping_Cart_Management" ,user = "postgres",
                            password = "Welcome@123", cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("The Database was connected succesfully")
        break

    except Exception as error:
        print("The Database connection failed")
        print("Error", error)

app.include_router(user.router)
app.include_router(admin.router)
app.include_router(Seller.router)
app.include_router(Customer.router)
app.include_router(review.router)
