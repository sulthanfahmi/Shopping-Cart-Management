from typing import List, Optional
from fastapi import  FastAPI,Response,status,HTTPException,Depends, APIRouter,File, UploadFile
from sqlalchemy.orm import Session 
from ..import models,schemas , oauth2 
from ..database import get_db
from typing import List
from PIL import Image
from fastapi.responses import JSONResponse
from sqlalchemy import and_



router = APIRouter(
    prefix = "/Seller",
    tags = ["Seller"]
)

@router.get("/",response_model = List[schemas.products])
def check_products(db: Session = Depends(get_db),
                   current_user : int = Depends(oauth2.get_current_user),
                   limit : int = 10, skip :int = 0, search : Optional[str] = "" ):
   
   print(limit) 
  
   posts = db.query(models.product).filter(models.product.owner_id == current_user.id,
        models.product.Products_name.contains(search)).limit(limit).offset(skip).all()
    
   if current_user.role != "1":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")


   return  posts 


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.products)
def add_products( post: schemas.add_Products, db: Session = Depends(get_db),
            current_user : int = Depends(oauth2.get_current_user)):
    
    New_Post = post.dict()
    
    if "owner_id" not in New_Post:
        New_Post["owner_id"] = current_user.id

    post = models.product(**New_Post)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")
   
    if current_user.role != "1":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/{id}", response_model = schemas.products)
def check_products(id : str,db: Session = Depends(get_db),
                   current_user : int = Depends(oauth2.get_current_user)):


    print(current_user)
    post = db.query(models.product).filter(and_(models.product.id == id, models.product.owner_id == current_user.id)).first()
    print(post)
    
    if not post:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail =  f"the post with id: {id} not found")
    
    if current_user.role != "1":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

       
    return post 


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_products(id : str, db: Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user)):

   
    print(current_user)

    post_query = db.query(models.product).filter(and_(models.product.id == id, models.product.owner_id == current_user.id)).first()

    if post_query == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"The post with id : {id} does not exists")
   
    if current_user.role != "1":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    
    db.delete(post_query)
        
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model = schemas.products)
def update_products(id : int , update_post:schemas.add_Products , db : Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user)):
     
    
    print(current_user)

    update_query = db.query(models.product).filter(and_(models.product.id == id, models.product.owner_id == current_user.id)).first()

  
    
    if update_query == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"The post with id : {id} does not exists")
    
    if current_user.role != "1":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    # Update the post
    db.query(models.product).filter(models.product.id == id).update(update_post.dict(), synchronize_session=False)
    db.commit()

    return update_query

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from sqlalchemy.orm import Session
import os

# Assume you have defined `get_db()` and `oauth2.get_current_user()` functions

# Mount the static files directory
router.mount("/static", StaticFiles(directory="C:/Users/sulthan fahmi/OneDrive/Desktop/Shopping Cart Management/static"), name="static")

@router.post("/upload/profile")
async def create_upload_file(file: UploadFile = File(...),
                             db: Session = Depends(get_db),
                             current_user: int = Depends(oauth2.get_current_user)):

    FILE_DIRECTORY = "C:/Users/sulthan fahmi/OneDrive/Desktop/Shopping Cart Management/static/images/"
    ALLOWED_EXTENSIONS = {"png", "jpg"}

    filename = file.filename
    extension = filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File extension not allowed")

    generate_name = os.path.join(FILE_DIRECTORY, filename)
    with open(generate_name, "wb") as new_file:
        new_file.write(file.file.read())

    try:
        img = Image.open(generate_name)
        img = img.resize(size=(200, 200))
        img.save(generate_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    # Constructing the file URL
    file_url = f"http://127.0.0.1:8000/static/images/{filename}"
    return {"message": "File uploaded successfully", "filename": file_url}


from fastapi import HTTPException, UploadFile, File, Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session
from PIL import Image
import os

@router.post("/uploadfile/product/{id}")
async def create_upload_file(id: int,
                              file: UploadFile = File(...),
                              db: Session = Depends(get_db),
                              current_user: int = Depends(oauth2.get_current_user)):
    FILE_DIRECTORY = "C:/Users/sulthan fahmi/OneDrive/Desktop/Shopping Cart Management/static/images/"
    ALLOWED_EXTENSIONS = {"png", "jpg"}

    filename = file.filename
    extension = filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File extension not allowed")

    generate_name = os.path.join(FILE_DIRECTORY, filename)
    with open(generate_name, "wb") as new_file:
        new_file.write(file.file.read())

        try:
            img = Image.open(generate_name)
            img = img.resize(size=(200, 200))
            img.save(generate_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    product = await product.get(id=id)
    business = await product.business
    owner = await business.owner

    if owner.id == current_user:
        product.product_image = filename
        await product.save()

    # Constructing the file URL
    file_url = f"http://127.0.0.1:8000/static/images/{filename}"
    return {"message": "File uploaded successfully", "filename": file_url}




    
    
