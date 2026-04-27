from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.database import get_db
from app.models.models import Look, UserPreference, User
from app.schemas.schemas import LookResponse, UserPreferenceRequest, UserCreate, UserResponse
from typing import Optional
from fastapi import Query
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.services.auth import authenticate_user, create_access_token, get_current_user
import bcrypt
import uuid

router = APIRouter()


@router.post("/token")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already taken")

    hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user = User(id=uuid.uuid4(), username=user.username, email=user.email, password_hash=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/looks", response_model=list[LookResponse])
def get_looks(db: Session = Depends(get_db), designer_id: Optional[uuid.UUID] = Query(None)):
    query = db.query(Look).options(joinedload(Look.designer))
    if designer_id:
        query = query.filter(Look.designer_id == designer_id)
    return query.all()


@router.get("/looks/{look_id}", response_model=LookResponse)
def get_look(look_id: uuid.UUID, db: Session = Depends(get_db)):
    look = db.query(Look).options(joinedload(Look.designer)).filter(Look.id == look_id).first()
    if not look:
        raise HTTPException(status_code=404, detail="Look not found")
    return look


@router.post("/user/preferences")
def save_preference(
    request: UserPreferenceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(UserPreference).filter_by(
        user_id=current_user.id, look_id=request.look_id
    ).first()
    if existing:
        existing.preference = request.preference
    else:
        db.add(UserPreference(
            id=uuid.uuid4(),
            user_id=current_user.id,
            look_id=request.look_id,
            preference=request.preference,
        ))
    db.commit()
    return {"ok": True}


@router.delete("/user/preferences/{look_id}")
def delete_preference(
    look_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    preference = db.query(UserPreference).filter_by(
        user_id=current_user.id, look_id=look_id
    ).first()
    if not preference:
        raise HTTPException(status_code=404, detail="Preference not found")
    db.delete(preference)
    db.commit()
    return {"ok": True}


@router.get("/user/preferences/status")
def get_preference_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, bool]:
    prefs = db.query(UserPreference).filter_by(user_id=current_user.id).all()
    return {str(p.look_id): p.preference for p in prefs}


@router.get("/user/preferences", response_model=list[LookResponse])
def get_user_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    looks = (
        db.query(Look)
        .options(joinedload(Look.designer))
        .join(UserPreference, Look.id == UserPreference.look_id)
        .filter(UserPreference.user_id == current_user.id, UserPreference.preference == True)
        .all()
    )
    return looks
