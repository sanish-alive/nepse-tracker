from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$", description="Username must be alphanumeric and can include underscores.")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128, description="Password must be at least 8 characters long.")

class UserUpdate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$", description="Username must be alphanumeric and can include underscores.")
    email: EmailStr

class PasswordUpdate(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=128, description="The current password of the user.")
    new_password: str = Field(..., min_length=8, max_length=128, description="The new password to update.")
    confirm_password: str = Field(..., min_length=8, max_length=128, description="The confirmation of the new password.")

class PriceTrackerItem(BaseModel):
    security_id: int
    min_target_price: float
    max_target_price: float
    status: bool