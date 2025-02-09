from typing import List, Optional
from fastapi import  FastAPI,Response,status,HTTPException,Depends, APIRouter,File
from sqlalchemy.orm import Session 
from ..import models,schemas , oauth2 
from ..database import get_db
from typing import List
from PIL import Image
from fastapi.responses import JSONResponse
from sqlalchemy import and_,ForeignKey

router = APIRouter(
    prefix = "/Reviews",
    tags = ["Reviews"]
)



@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.review_call)
def add_products( post: schemas.Review, db: Session = Depends(get_db),
            current_user : int = Depends(oauth2.get_current_user)):
    
    New_Post = post.dict()

    
    
    if "owner_id" not in New_Post:
        New_Post["owner_id"] = current_user.id

    post = models.Customer_Reviews(**New_Post)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")
   
    if current_user.role != "2":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/",response_model = List[schemas.review_call])
def check_products(db: Session = Depends(get_db),
                   current_user : int = Depends(oauth2.get_current_user),
                   limit : int = 10, skip :int = 0, search : Optional[str] = "" ):
   
   print(limit) 
  
   posts = db.query(models.Customer_Reviews).filter(models.Customer_Reviews.owner_id == current_user.id,
        models.Add_To_Cart.Products_name.contains(search)).limit(limit).offset(skip).all()
    
   if current_user.role != "2":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")


   return  posts 

@router.get("/{id}", response_model = schemas.review_call)
def check_products(id : str,db: Session = Depends(get_db),
                   current_user : int = Depends(oauth2.get_current_user)):


    print(current_user)
    post = db.query(models.Customer_Reviews).filter(and_(models.Customer_Reviews.id == id, models.Customer_Reviews.owner_id == current_user.id)).first()
    print(post)
    
    if not post:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail =  f"the post with id: {id} not found")
    
    if current_user.role != "2":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

       
    return post 

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_products(id : str, db: Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user)):

   
    print(current_user)

    post_query = db.query(models.Customer_Reviews).filter(and_(models.Customer_Reviews.id == id, models.Customer_Reviews.owner_id == current_user.id)).first()

    if post_query == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"The post with id : {id} does not exists")
   
    if current_user.role != "2":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    
    db.delete(post_query)
        
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model = schemas.review_call)
def update_products(id : int , update_post:schemas.update_review , db : Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user)):
     
    
    print(current_user)

    update_query = db.query(models.Customer_Reviews).filter(and_(models.Customer_Reviews.id == id, models.Customer_Reviews.owner_id == current_user.id)).first()

  
    
    if update_query == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"The post with id : {id} does not exists")
    
    if current_user.role != "2":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    # Update the post
    db.query(models.Customer_Reviews).filter(models.Customer_Reviews.id == id).update(update_post.dict(), synchronize_session=False)
    db.commit()

    return update_query

