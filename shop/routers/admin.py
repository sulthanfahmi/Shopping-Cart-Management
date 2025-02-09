from fastapi import  Response,status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import  database,schemas, models, utils , oauth2 
from datetime import datetime, timedelta


from ..database import get_db 

router = APIRouter(
    prefix = "/admin",
    tags = ["Admin"])

from fastapi import HTTPException, status

@router.post("/", response_model=schemas.Token)
def login(user_credentials: schemas.VerifyEmail, db: Session = Depends(database.get_db)):

    # Check if the OTP provided by the user matches the OTP stored in the database
    user_db = db.query(models.user).filter(models.user.email == user_credentials.email).first()

    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_db.otp != user_credentials.otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
    
    # Generate access token
    access_token = oauth2.create_access_token(data={"user_id": user_db.id})
    
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/send_otp")
def send_otp_to_email(userotp: schemas.user, db: Session = Depends(get_db)):

    user_otp = db.query(models.user).filter(models.user.email == userotp.email).first()

    if not user_otp:
        raise HTTPException(status_code=404, detail="Email not found")
    
    otp = oauth2.generate_otp()
    oauth2.send_otp(userotp.email, otp)


    # Store OTP in the database (assuming you have an "otp" column in your User model)

    user_otp.otp = otp
    db.commit()
    
    return {"message": "OTP sent successfully"}


@router.post("/verify_otp")
def verify_otp(verifying_otp: schemas.VerifyEmail, db: Session = Depends(get_db)):

    # Check if the OTP provided by the user matches the OTP stored in the database
    user_db = db.query(models.user).filter(models.user.email == verifying_otp.email).first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if user_db.otp != verifying_otp.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {"message": "OTP verified successfully"}