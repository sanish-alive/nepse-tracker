import os
from dotenv import load_dotenv
import security
from typing import Annotated
from fastapi import Body, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from nepse import Nepse
from database import DatabaseManager

load_dotenv()

# nepse = Nepse()
# nepse.setTLSVerification(False)
# today_price = nepse.getPriceVolumeHistory(datetime.date.today())
# print(today_price)

# symbol = input('Enter Symbol: ').upper()
# min_price = float(input('Enter Minimum Price: '))
# max_price = float(input('Enter Maximum Price: '))
# email = input('Enter Email: ')

class PriceTrackerItem(BaseModel):
    symbol: str
    min_target_price: float
    max_target_price: float
    email: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$", description="Username must be alphanumeric and can include underscores.")
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

@app.get("/")
async def root():
    return {"message": "Welcome to Nepse Tracker"}

@app.post("/signup")
async def signUp(item: Annotated[UserRegistration, Body(embed=True)]):
    try:
        db = DatabaseManager()
        password = security.getPasswordHash(item.password)
        db.insertUser(item.username, item.email, password)
        return {"message": "User registered successfully!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/signin")
async def signIn(request: LoginRequest):
    try:
        db = DatabaseManager()
        user = db.getUser(request.email)
        if user:
            if security.verfiyPassword(request.password, user['password']):
                data = {
                    "username": user["username"],
                    "email": user["email"]
                }
                token = security.createAccessToken(data)
                return {"message": "Login success.", "token": token}
            else:
                return {"message": "Login failed."}
        else:
            return {"message": "No such user exists"}
    except Exception as e:
        return {"error": "login error"}
    

@app.post("/price-tracker")
async def priceTracker(item: Annotated[PriceTrackerItem, Body(embed=True)]):
    db = DatabaseManager()
    db.insertData(item.symbol, item.min_price, item.max_price, item.email)
    return item.symbol