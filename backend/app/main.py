from fastapi import FastAPI
from app.api.routes import router
from app.models.database import engine, Base
from app.models.models import User, Designer, Look, UserPreference, Recommendation  # Import models explicitly

app = FastAPI()

# Create tables if they don’t exist
Base.metadata.create_all(bind=engine)

# Register API routes
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to the Fashion Bug API!"}
