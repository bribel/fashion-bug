from sqlalchemy import Column, String, Boolean, ForeignKey, Float, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.models.base import Base


# Users Table
class User(Base):
    __tablename__ = "users"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)

    # Relationships
    preferences = relationship("UserPreference", back_populates="user", cascade="all, delete")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

# Designers Table
class Designer(Base):
    __tablename__ = "designers"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)

    # Relationship to looks
    looks = relationship("Look", back_populates="designer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Designer(id={self.id}, name={self.name})>"

# Looks Table (Runway images, linked to designers)
class Look(Base):
    __tablename__ = "looks"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    designer_id = Column(PG_UUID(as_uuid=True), ForeignKey("designers.id", ondelete="CASCADE"), nullable=False)
    season = Column(String(20))
    gender = Column(String(10), nullable=False)  
    collection_type = Column(String(20), nullable=False)  # "Ready-to-Wear", "Haute Couture"
    image_url = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=True)  
    created_at = Column(TIMESTAMP, default=func.now(), nullable=True)

    # Relationships
    designer = relationship("Designer", back_populates="looks")
    preferences = relationship("UserPreference", back_populates="look", cascade="all, delete")
    recommendations = relationship("Recommendation", back_populates="look", cascade="all, delete")

    def __repr__(self):
        return f"<Look(id={self.id}, designer_id={self.designer_id}, season={self.season})>"

# User Preferences Table (Likes/Dislikes)
class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    look_id = Column(PG_UUID(as_uuid=True), ForeignKey("looks.id", ondelete="CASCADE"), nullable=False)
    preference = Column(Boolean, nullable=False)  # True = Liked, False = Disliked
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="preferences")
    look = relationship("Look", back_populates="preferences")

    def __repr__(self):
        return f"<UserPreference(id={self.id}, user_id={self.user_id}, look_id={self.look_id}, preference={self.preference})>"

# Recommendations Table
class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    look_id = Column(PG_UUID(as_uuid=True), ForeignKey("looks.id", ondelete="CASCADE"), nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="recommendations")
    look = relationship("Look", back_populates="recommendations")

    def __repr__(self):
        return f"<Recommendation(id={self.id}, user_id={self.user_id}, look_id={self.look_id}, confidence_score={self.confidence_score})>"
