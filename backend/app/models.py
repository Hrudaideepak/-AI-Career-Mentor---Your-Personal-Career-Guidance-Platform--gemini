from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat_sessions = relationship("ChatSession", back_populates="user")
    resumes = relationship("Resume", back_populates="user")
    career_recommendations = relationship("CareerRecommendation", back_populates="user")
    progress_tracking = relationship("ProgressTracking", back_populates="user")
    roadmaps = relationship("Roadmap", back_populates="user")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_number = Column(Integer, nullable=False, default=1)  # Per-user session number (1-10)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True) # Link to specific resume
    created_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(String, nullable=True)

    user = relationship("User", back_populates="chat_sessions")
    resume = relationship("Resume")
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    user_id = Column(Integer, ForeignKey("users.id")) # Redundant but useful for quick access
    role = Column(String) # user/assistant
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String)
    parsed_content = Column(Text) # JSON string or raw text
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")

class CareerRecommendation(Base):
    __tablename__ = "career_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    career_name = Column(String)
    reasoning = Column(Text)
    salary_range = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="career_recommendations")

class ProgressTracking(Base):
    __tablename__ = "progress_tracking"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_name = Column(String)
    score = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress_tracking")

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    career_id = Column(Integer, ForeignKey("career_recommendations.id"), nullable=True) # Link to specific recommendation
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="roadmaps")
    steps = relationship("RoadmapStep", back_populates="roadmap")

class RoadmapStep(Base):
    __tablename__ = "roadmap_steps"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"))
    step_name = Column(String)
    status = Column(String, default="pending") # pending/completed
    completion_date = Column(DateTime, nullable=True)

    roadmap = relationship("Roadmap", back_populates="steps")
