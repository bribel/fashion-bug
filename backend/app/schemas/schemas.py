from pydantic import BaseModel, EmailStr
import uuid
from typing import Optional


class DesignerResponse(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True


class LookResponse(BaseModel):
    id: uuid.UUID
    designer_id: uuid.UUID
    designer: Optional[DesignerResponse] = None
    season: Optional[str] = None
    gender: str
    collection_type: str
    image_url: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class UserPreferenceRequest(BaseModel):
    look_id: uuid.UUID
    preference: bool  # True = liked, False = disliked


class UserPreferenceResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    look_id: uuid.UUID
    preference: bool

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str

    class Config:
        from_attributes = True
