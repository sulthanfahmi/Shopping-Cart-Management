from typing import List, Optional
from fastapi import  FastAPI,Response,status,HTTPException,Depends, APIRouter,File, UploadFile
from sqlalchemy.orm import Session 
from ..import models,schemas , oauth2 
from ..database import get_db
from typing import List
from PIL import Image
from fastapi.responses import JSONResponse
from sqlalchemy import and_,ForeignKey



router = APIRouter(
    prefix = "/customer",
    tags = ["Customer"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_to_cart_and_buy(post: schemas.Customer, db: Session = Depends(get_db),
                         current_user: schemas.user = Depends(oauth2.get_current_user)):

    new_post_data = post.dict()

    if "current_user" not in new_post_data:
        new_post_data["current_user"] = current_user.id

    # Create an instance of Add_To_Cart
    new_post = models.Add_To_Cart(**new_post_data)

    if new_post.current_user != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    # Query the Product table to find the product by its name
    product = db.query(models.product).filter(models.product.Products_name == new_post.Products_name).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Check user authorization
    if current_user.role != "2":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")
    
    new_post.category_products = product.category
    new_post.original_price = product.original_price
    new_post.new_price = product.new_price

    # Add the new post to the database
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Prepare the response data
    response_details = schemas.Buy(category_products=product.category,
                           original_price=product.original_price,
                           new_price=product.new_price,
                           current_user=new_post.current_user)
    response_data = schemas.Details_List(Products_name=new_post.Products_name, Details=response_details)

    return response_data



@router.get("/",response_model = List[schemas.cart])
def Go_To_Cart(db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user),
                   limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(limit) 

    post = db.query(models.Add_To_Cart).filter(models.Add_To_Cart.current_user == current_user.id,
        models.Add_To_Cart.Products_name.contains(search)).limit(limit).offset(skip).all()

    if current_user.role != "2":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    return post



@router.get("/{id}", response_model = schemas.cart)
def Go_TO_Cart(id : str ,db: Session = Depends(get_db),
                   current_user : int = Depends(oauth2.get_current_user)):


    print(current_user)
    post = db.query(models.Add_To_Cart).filter(and_(models.Add_To_Cart.id == id,
                                 models.Add_To_Cart.current_user == current_user.id)).first()
    print(post)

  
    
    if not post:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail =  f"the post with id: {id} not found")
    
    if current_user.role != "2":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

       
    return post 

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_Cart_Items(id : str , db: Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user)):

   
    print(current_user)

    post_query = db.query(models.Add_To_Cart).filter(and_(models.Add_To_Cart.id == id, 
                                        models.Add_To_Cart.current_user == current_user.id)).first()

    if post_query == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"The post with id : {id} does not exists")
   
    if current_user.role != "2":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    
    db.delete(post_query)
        
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/", status_code=status.HTTP_201_CREATED)
def Add_More(post: schemas.Customer, db: Session = Depends(get_db),
                         current_user: schemas.user = Depends(oauth2.get_current_user)):

    new_post_data = post.dict()

    if "current_user" not in new_post_data:
        new_post_data["current_user"] = current_user.id

    # Create an instance of Add_To_Cart
    new_post = models.Add_To_Cart(**new_post_data)

    if new_post.current_user != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    # Query the Product table to find the product by its name
    product = db.query(models.product).filter(models.product.Products_name == new_post.Products_name).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Check user authorization
    if current_user.role != "2":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")
    
    new_post.category_products = product.category
    new_post.original_price = product.original_price
    new_post.new_price = product.new_price

    # Add the new post to the database
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Prepare the response data
    response_details = schemas.Buy(category_products=product.category,
                           original_price=product.original_price,
                           new_price=product.new_price,
                           current_user=new_post.current_user)
    response_data = schemas.Details_List(Products_name=new_post.Products_name, Details=response_details)

    return response_data
