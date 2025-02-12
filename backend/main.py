from dotenv import load_dotenv
import security
from typing import Annotated
from fastapi import Body, FastAPI, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import DatabaseManager
import schemas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

@app.get("/")
async def root():
    return {"message": "Welcome to Nepse Tracker"}

@app.get("/online")
async def apiTest():
    return {"message": "Nepse Tracker API is working..."}

@app.post("/signup")
async def signUp(item: Annotated[schemas.UserRegistration, Body(embed=True)]):
    try:
        db = DatabaseManager()
        password = security.getPasswordHash(item.password)
        db.insertUser(item.username, item.fullname, item.email, password)
        return {"message": "User registered successfully!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/signin")
async def signIn(response: Response, request: schemas.LoginRequest):
    try:
        db = DatabaseManager()
        user = db.getUser(request.email)
        if user:
            if security.verfiyPassword(request.password, user['password']):
                data = {
                    "username": user["username"],
                    "fullname": user["fullname"],
                    "email": user["email"]
                }
                token = security.createAccessToken(data)
                response.set_cookie(
                    key="access_token",
                    value=token,
                    httponly=True,
                    secure=False,
                    samesite="Strict"
                )
                return {"message": "Login success.", "token": token}
            else:
                return {"message": "Login failed."}
        else:
            return {"message": "No such user exists"}
    except Exception as e:
        return {"error": "login error"}
    
@app.get("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "logged out successfully"}

@app.get("/profile")
async def getUser(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    payload = security.verifyToken(access_token)
    if payload:
        db = DatabaseManager()
        user = db.getUser(payload['email'])
        data = {
            "username": user['username'],
            "fullname": user['fullname'],
            "email": user["email"],
            "updatedat": user['updated_at'],
            "createdat": user['created_at']
        }
        return data
    else:
        raise HTTPException(status_code=401, detail="Invalid Token")

@app.post("/profile/update")
async def updateProfile(request: Request, user_detail: schemas.UserUpdate):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    payload = security.verifyToken(access_token)
    if payload:
        db = DatabaseManager()
        user = db.getUser(payload['email'])
        db.updateUser(user['id'], user_detail.username, user.fullname, user_detail.email)
        return {"message": "User detail is updated"}
    else:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
@app.get("/price-tracker")
async def getPriceTracker(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    payload = security.verifyToken(access_token)
    if payload:
        db = DatabaseManager()
        user = db.getUser(payload['email'])
        price_tracks = db.geAllUserPriceTracker(user['id'])

        return price_tracks
    else:
        raise HTTPException(status_code=401, detail="Invalid Token")

@app.post("/price-tracker")
async def storePriceTracker(request: Request, item: Annotated[schemas.PriceTrackerItem, Body(embed=True)]):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    payload = security.verifyToken(access_token)
    if payload:
        db = DatabaseManager()
        user= db.getUser(payload['email'])
        db.storePriceTracker(user['id'], item.security_id, item.min_target_price, item.max_target_price, item.status)
        return {"message": "price is track is added."}
    else:
        raise HTTPException(status_code=401, detail="Invalid Token")