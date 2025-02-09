from jose import JWTError, jwt
from datetime import datetime , timedelta
from fastapi import Depends,status,HTTPException ,FastAPI
from .import schemas,database,models
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials


from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from typing import Optional

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
bearer_scheme = HTTPBearer()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    
    return payload

def get_current_user(token: str = Depends(bearer_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        token_data = verify_access_token(token.credentials, credentials_exception)
        user = db.query(models.user).filter(models.user.id == token_data['user_id']).first()
        if user is None:
            raise credentials_exception
        return user
    except AttributeError:
        raise credentials_exception
 

# Default sender email configuration
DEFAULT_SENDER_EMAIL = "sulthan.22msd7002@vitapstudent.ac.in"  
SMTP_SERVER = "smtp.gmail.com"
SMTP_USERNAME = "sulthanfahmi628@gmail.com"  # Update with your Gmail address
SMTP_PASSWORD = "begu rssq upog rzkk"  # Update with your Gmail app password
SMTP_PORT = 587


# Function to send OTP via email
def send_otp(email: str, otp: str):
    # Create message
    sender_email = SMTP_USERNAME
    receiver_email = email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = 'OTP'

    # Body of the email
    body = f"Your OTP is: {otp}"
    message.attach(MIMEText(body, "plain"))

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)

# Function to generate OTP
def generate_otp():
# Generate a 6-digit OTP
    return str(randint(100000, 999999))



