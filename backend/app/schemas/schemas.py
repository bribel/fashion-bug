from pydantic import BaseModel, EmailStr
import uuid
from typing import Optional

# Schema for returning Look data
class LookResponse(BaseModel):
    id: uuid.UUID
    designer_id: uuid.UUID
    season: str
    gender: str
    collection_type: str
    image_url: str
    description: Optional[str] = None  # Optional field

    class Config:
        from_attributes = True

# Schema for creating a new user preference (liking/disliking a look)
class UserPreferenceRequest(BaseModel):
    user_id: uuid.UUID
    look_id: uuid.UUID
    preference: bool  # True = Liked, False = Disliked

# Schema for returning a user's preferences
class UserPreferenceResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    look_id: uuid.UUID
    preference: bool

    class Config:
        from_attributes = True

# Schema for user registration
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Plain text password for input

# Schema for returning user data (excluding password)
class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str

    class Config:
        from_attributes = True  # Ensures SQLAlchemy compatibility