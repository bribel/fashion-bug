from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.models.models import User
from app.models.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
import bcrypt
import uuid

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Secret key for signing JWT tokens
SECRET_KEY = "your_secret_key"  # Replace with a strong secret in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password

# Function to verify the password with bcrypt
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Check if the entered password matches the hashed password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Function to verify user credentials
def authenticate_user(db: Session, email: str, password: str):
    # Fetch user from database by email
    user = db.query(User).filter(User.email == email).first()
    
    # If user doesn't exist or password doesn't match the hashed password
    if not user or not verify_password(password, user.password_hash):
        return None
    
    return user

# Function to generate a JWT access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to get the current logged-in user
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: uuid.UUID = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
