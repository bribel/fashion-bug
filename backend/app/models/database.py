from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
from app.models.base import Base  # noqa: F401
from app.models.models import Designer, Look

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Create backend/.env from .env.example.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_or_create_designer(db_session: Session, designer_name: str):
    designer = db_session.query(Designer).filter(Designer.name == designer_name).first()
    if designer:
        return designer.id
    new_designer = Designer(name=designer_name)
    db_session.add(new_designer)
    db_session.flush()
    return new_designer.id


def save_to_db(db_session: Session, img_url: str, designer_name: str, season: str, collection_type: str, description: str, gender: str):
    try:
        designer_id = get_or_create_designer(db_session, designer_name)
        new_look = Look(
            image_url=img_url,
            designer_id=designer_id,
            season=season,
            collection_type=collection_type,
            description=description,
            gender=gender,
        )
        db_session.add(new_look)
        db_session.commit()
        print(f"Look saved to DB: {img_url}")
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error saving look to DB: {str(e)}")
