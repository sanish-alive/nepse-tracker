import uvicorn
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
            if security.verifyPassword(request.password, user['password']):
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
                    secure=True,
                    samesite="Strict"
                )
                print('login success')
                return {"login": True, "message": "Login success.", "token": token}
            else:
                return {"login": False, "message": "Invalid Credentials"}
        else:
            return {"login": False, "message": "Invalid Credentials"}
    except Exception as e:
        print(f"login error: {e}")
        return {"login": False, "message": "Something went wrong. Please try again."}
    

@app.get("/auth/check")
async def authCheck(request: Request):
    return {"authenticated": True} if security.isAuthenticated(request) else {"authenticated": False}


@app.post("/logout")
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
        data = []
        for pr in price_tracks:
            stock = db.getSecurity(pr["security_id"])
            data.append({
                "id": pr["id"],
                "symbol": stock['symbol'],
                "name": stock["security_name"],
                "security_id": pr["security_id"],
                "min_price": pr["min_target_price"],
                "max_price": pr["max_target_price"],
                "created_at": pr["created_at"],
                "status": pr["status"]
            })

        return data
    else:
        raise HTTPException(status_code=401, detail="Invalid Token")

@app.post("/price-tracker")
async def storePriceTracker(request: Request, item: schemas.PriceTrackerItem):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    payload = security.verifyToken(access_token)
    if payload:
        db = DatabaseManager()
        user= db.getUser(payload['email'])
        print(item)
        db.storePriceTracker(user['id'], item.security_id, item.min_target_price, item.max_target_price, item.status)
        return {"message": "price is track is added."}
    else:
        raise HTTPException(status_code=401, detail="Invalid Token!")
    
@app.put("/price-tracker")
async def updatePriceTracker(request: Request, item: schemas.UpdatePriceTrackerItem):
    payload = security.isAuthenticated(request)
    if payload:
        print(item.status)
        db = DatabaseManager()
        user = db.getUser(payload["email"])
        db.updatePriceTracker(item.alert_id, user['id'], item.security_id, item.min_target_price, item.max_target_price, item.status)
        return {"message": "Price Tracke is updated."}
    else:
        raise HTTPException(status_code=401, detail="Invalid Token!")
    
@app.delete("/price-tracker")
async def destroyPriceTracker(request: Request, item: schemas.DestroyPriceTrakcerItem):
    payload = security.isAuthenticated(request)
    if payload:
        db = DatabaseManager()
        user = db.getUser(payload["email"])
        db.destroyPriceTracker(user['id'], item.alert_id)
        return {"status": True}
    else:
        return {"status": False}
    
@app.get("/securities")
async def securities(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    payload = security.verifyToken(access_token)
    if payload:
        db = DatabaseManager()
        security_list = db.getAllSecurities()
        return security_list
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)