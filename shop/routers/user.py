from typing import List
from fastapi import  FastAPI,Response,status,HTTPException,Depends, APIRouter, BackgroundTasks 
from sqlalchemy.orm import Session 
from ..import models,schemas,utils,oauth2

from ..database import get_db 

router = APIRouter(
    prefix = "/user",
    tags = ["User"]
)

# For the table name user 

@router.post("/", status_code=status.HTTP_201_CREATED,response_model = schemas.display)
def create_user(user : schemas.usercreate,db: Session = Depends(get_db)):
     
    hash_Password = utils.hash(user.password)
    user.password = hash_Password

    
    new_user = models.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_user(id : str, db: Session = Depends(get_db)):

    user = db.query(models.user).filter(models.user.id == id)  


    if user.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"The post with id : {id} does not exists")
    user.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model = schemas.display)
def update_user(id : int ,update_user:schemas.updateUser,db: Session = Depends(get_db)):
     
   
    user_updatetable = db.query(models.user).filter(models.user.id == id)
    useres = user_updatetable.first()
    if useres == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"The post with id : {id} does not exists")
    user_updatetable.update(update_user.dict(),synchronize_session = False)
    db.commit()
    return user_updatetable.first()

@router.get("/",response_model = List[schemas.display],openapi_extra={"x-aperture-labs-portal": "blue"})
def get_user(db: Session = Depends(get_db)):
    
    user_get = db.query(models.user).all()
    return  user_get

@router.get("/{id}", response_model = schemas.display )
def get_id(id : int , db: Session = Depends(get_db)):
    
    user = db.query(models.user).filter(models.user.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"The post with id : {id} does not exists")
    return  user 
