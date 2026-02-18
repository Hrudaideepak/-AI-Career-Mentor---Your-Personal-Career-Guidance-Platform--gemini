from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database, models
from ..services import openai_service, chroma_service

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sessions/", response_model=schemas.ChatSession)
def create_session(session: schemas.ChatSessionCreate, db: Session = Depends(get_db)):
    return crud.create_chat_session(db, session)

@router.get("/sessions/{user_id}")
def get_sessions(user_id: int, db: Session = Depends(get_db)):
    return crud.get_chat_sessions(db, user_id)

@router.get("/history/{session_id}")
def get_messages(session_id: int, db: Session = Depends(get_db)):
    return crud.get_chat_messages(db, session_id)

@router.post("/messages/", response_model=schemas.ChatMessage)
async def create_message(message: schemas.ChatMessageCreate, db: Session = Depends(get_db)):
    # Save user message
    db_message = crud.create_chat_message(db, message)
    
    # Add to ChromaDB
    chroma_service.add_chat_to_vector_store(message.content, str(message.user_id), str(message.session_id), str(db_message.id))
    
    # --- Build rich context for AI ---
    
    # 1. Resume context
    current_session = db.query(models.ChatSession).filter(models.ChatSession.id == message.session_id).first()
    
    resume_id = None
    if current_session and current_session.resume_id:
        resume_id = str(current_session.resume_id)
    else:
        latest_resume = crud.get_latest_resume(db, message.user_id)
        resume_id = str(latest_resume.id) if latest_resume else None
    
    resume_context = chroma_service.query_resume_context(message.content, str(message.user_id), resume_id=resume_id)
    
    # 2. Current session context (recent conversation flow)
    history_context = chroma_service.query_chat_history(message.content, str(message.session_id))
    
    # 3. Cross-session user context (what user discussed in ALL past sessions)
    cross_session_context = chroma_service.query_user_chat_history(message.content, str(message.user_id))
    
    # 4. Get user profile info
    user = db.query(models.User).filter(models.User.id == message.user_id).first()
    user_profile = f"Username: {user.username}, Email: {user.email}" if user else ""
    
    # 5. Get summaries of all user sessions for broader awareness
    all_sessions = crud.get_chat_sessions(db, message.user_id)
    session_summaries = "\n".join([
        f"Session {s.session_number}: {s.summary or 'No summary'}"
        for s in all_sessions
    ])
    
    # 6. Call OpenAI with full context
    ai_response_text = await openai_service.generate_chat_response(
        message.content, history_context, resume_context,
        cross_session_context=cross_session_context,
        user_profile=user_profile,
        session_summaries=session_summaries
    )
    
    # 7. Store AI response
    assistant_message_data = schemas.ChatMessageCreate(
        session_id=message.session_id,
        user_id=message.user_id,
        role="assistant",
        content=ai_response_text
    )
    db_assistant_message = crud.create_chat_message(db, assistant_message_data)
    
    # 8. Add to ChromaDB
    chroma_service.add_chat_to_vector_store(
        ai_response_text, 
        str(message.user_id), 
        str(message.session_id), 
        str(db_assistant_message.id)
    )
    
    return db_assistant_message
