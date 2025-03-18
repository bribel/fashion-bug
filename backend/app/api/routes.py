from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.models import Look, UserPreference, User
from app.schemas.schemas import LookResponse, UserPreferenceRequest, UserCreate, UserResponse
from typing import Optional
from fastapi import Query
import bcrypt
import uuid

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all looks
@router.get("/looks", response_model=list[LookResponse])
def get_looks(db: Session = Depends(get_db), designer_id: Optional[uuid.UUID] = Query(None)):
    query = db.query(Look)
    if designer_id:
        query = query.filter(Look.designer_id == designer_id)
    return query.all()

# Get look by ID
@router.get("/looks/{look_id}", response_model=LookResponse)
def get_look(look_id: uuid.UUID, db: Session = Depends(get_db)):
    look = db.query(Look).filter(Look.id == look_id).first()
    if not look:
        raise HTTPException(status_code=404, detail="Look not found")
    return look

# Save a user’s like/dislike for a look
@router.post("/user/preferences", response_model=UserPreferenceRequest)
def save_user_preference(request: UserPreferenceRequest, db: Session = Depends(get_db)):
    preference = UserPreference(
        id=uuid.uuid4(),
        user_id=request.user_id,
        look_id=request.look_id,
        preference=request.preference
    )
    db.add(preference)
    db.commit()
    db.refresh(preference)  # Refresh to get updated data
    return preference


# Get all liked looks for a user
@router.get("/user/preferences/{user_id}", response_model=list[LookResponse])
def get_user_preferences(user_id: uuid.UUID, db: Session = Depends(get_db)):
    looks = (
        db.query(Look)
        .join(UserPreference, Look.id == UserPreference.look_id)
        .filter(UserPreference.user_id == user_id, UserPreference.preference == True)
        .all()
    )
    return looks

# Create a new user
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already taken")

    # Hash the password before storing
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    # Create new user
    new_user = User(
        id=uuid.uuid4(),
        username=user.username,
        email=user.email,
        password_hash=hashed_password.decode("utf-8")  # Convert bytes to string
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user