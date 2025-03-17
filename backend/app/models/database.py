from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
from app.models.models import Designer, Look
from app.models.base import Base  # Import Base from the new file

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Tree1231@localhost:5432/fashionbug_db")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for defining models
# Base = declarative_base()

def get_or_create_designer(db_session: Session, designer_name: str):
    """
    Check if a designer exists by name. If it doesn't exist, create a new designer and return the ID.
    """
    # Check if the designer already exists
    designer = db_session.query(Designer).filter(Designer.name == designer_name).first()
    
    if designer:
        # If designer exists, return the existing designer_id
        return designer.id
    else:
        # If designer does not exist, create a new designer
        new_designer = Designer(name=designer_name)
        db_session.add(new_designer)
        db_session.flush()

        # Return the new designer's id
        return new_designer.id
    
# Save data to database function
def save_to_db(db_session: Session, img_url: str, designer_name: str, season: str, collection_type: str, description: str, gender: str):
    """
    Save the scraped image data and collection details to the database.
    """
    try:
        # Get or create the designer and get the designer_id
        designer_id = get_or_create_designer(db_session, designer_name)

        # Create a new Look instance
        new_look = Look(
            image_url=img_url,
            designer_id=designer_id,  # Designer ID should be passed when calling this function
            season=season,
            collection_type=collection_type,
            description=description,
            gender=gender
        )

        # Add and commit to the database
        db_session.add(new_look)
        db_session.commit()

        print(f"✅ Look saved to DB: {img_url}")

    except SQLAlchemyError as e:
        db_session.rollback()  # Rollback in case of error
        print(f"⚠ Error saving look to DB: {str(e)}")