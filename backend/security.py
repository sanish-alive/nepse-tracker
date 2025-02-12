import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import HTTPException
import jwt
from datetime import datetime, timedelta, timezone

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verfiyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def getPasswordHash(password):
    return pwd_context.hash(password)

def createAccessToken(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm = os.getenv('ALGORITHM'))
    return encoded_jwt

def verifyToken(token: str):
    try:
        payload = jwt.decode(
            token,
            os.getenv('SECRET_KEY'),
            algorithms=[os.getenv('ALGORITHM')],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")