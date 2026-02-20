from app.db.models import User
from app.db.db import get_db
from app.models.auth import RegisterUser, UserDetails
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
import jwt
import bcrypt
import os
import dotenv
from datetime import datetime, timezone, timedelta

dotenv.load_dotenv()
router = APIRouter()

secret=os.environ.get("JWT_SECRET") | "dkjfaidfjei4ou9028ruq208mxuHHDUFGHjfeu9!#@*u9fj"
algorithm=os.environ.get("HASH_ALGORITHM") | "SHA256"
expiry_time=int(os.environ.get("EXPIRY_TIME")) | 1

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def generate_access_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=expiry_time)
    }
    token = jwt.encode(payload, secret, algorithm)
    return token

@router.get("/register/")
def register(data: RegisterUser, db: Session = Depends(get_db)):
    hashed_password = hash_password(data.password)
    user = User(username=data.username, email=data.email, name=data.name, password=hashed_password)
    try:
        db.add(user)
        db.commit()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to add user")
    return user

@router.get("/login/", response_model=UserDetails)
def login(password: str, email: str | None=None, username: str | None = None, db: Session = Depends(get_db)):
    if not email and not username:
        raise HTTPException(status_code=400, detail="Require either username or email")
    query = select(User).where(User.username==username or User.email==email)
    try: 
        user = db.execute(query).scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="No user found")
        if not bcrypt.checkpw(password.encode(),user.password.encode()): 
            raise HTTPException(status_code=403, detail="Incorrect password")
        return user
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch user")