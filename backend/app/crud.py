from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_chat_session(db: Session, session: schemas.ChatSessionCreate):
    # Count existing sessions for this user
    user_sessions = db.query(models.ChatSession).filter(
        models.ChatSession.user_id == session.user_id
    ).order_by(models.ChatSession.session_number.asc()).all()
    
    session_count = len(user_sessions)
    
    # If user already has 10 sessions, delete the oldest one (and its messages)
    if session_count >= 10:
        oldest_session = user_sessions[0]
        db.query(models.ChatMessage).filter(
            models.ChatMessage.session_id == oldest_session.id
        ).delete()
        db.delete(oldest_session)
        db.commit()
        # Renumber remaining sessions 1-9
        remaining = db.query(models.ChatSession).filter(
            models.ChatSession.user_id == session.user_id
        ).order_by(models.ChatSession.created_at.asc()).all()
        for i, s in enumerate(remaining, start=1):
            s.session_number = i
        db.commit()
        next_number = 10
    else:
        next_number = session_count + 1
    
    db_session = models.ChatSession(
        user_id=session.user_id,
        session_number=next_number,
        summary=session.summary
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def update_chat_session(db: Session, session_id: int, resume_id: int = None, summary: str = None):
    session = db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
    if session:
        if resume_id:
            session.resume_id = resume_id
        if summary:
            session.summary = summary
        db.commit()
        db.refresh(session)
    return session

def get_chat_sessions(db: Session, user_id: int):
    return db.query(models.ChatSession).filter(
        models.ChatSession.user_id == user_id
    ).order_by(models.ChatSession.session_number.asc()).all()

def get_all_user_chat_messages(db: Session, user_id: int, limit: int = 50):
    """Get recent messages across ALL sessions for a user, for cross-session context."""
    return db.query(models.ChatMessage).filter(
        models.ChatMessage.user_id == user_id
    ).order_by(models.ChatMessage.timestamp.desc()).limit(limit).all()

def create_chat_message(db: Session, message: schemas.ChatMessageCreate):
    db_message = models.ChatMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_chat_messages(db: Session, session_id: int):
    return db.query(models.ChatMessage).filter(models.ChatMessage.session_id == session_id).order_by(models.ChatMessage.timestamp).all()

def create_resume(db: Session, resume: schemas.ResumeCreate):
    db_resume = models.Resume(**resume.dict())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def create_career_recommendation(db: Session, recommendation: schemas.CareerRecommendationCreate):
    db_recommendation = models.CareerRecommendation(**recommendation.dict())
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation

def get_latest_resume(db: Session, user_id: int):
    return db.query(models.Resume).filter(models.Resume.user_id == user_id).order_by(models.Resume.uploaded_at.desc()).first()
