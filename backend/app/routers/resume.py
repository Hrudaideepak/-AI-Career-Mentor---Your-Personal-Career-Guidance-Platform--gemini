from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database
from ..services import parser_service, openai_service, chroma_service
import shutil
import os
from pathlib import Path

# Always resolve to project_root/data/resumes regardless of working directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RESUMES_DIR = PROJECT_ROOT / "data" / "resumes"

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/{user_id}", response_model=schemas.Resume)
async def upload_resume(user_id: int, session_id: int = None, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save file locally (optional, but good for persistence)
    upload_dir = RESUMES_DIR / str(user_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = str(upload_dir / file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Reset file pointer after reading
    await file.seek(0)
    
    # Parse generic file content
    parsed_text = await parser_service.parse_resume(file)
    
    # Create DB entry
    resume_data = schemas.ResumeCreate(user_id=user_id, file_path=file_path, parsed_content=parsed_text)
    db_resume = crud.create_resume(db, resume_data)
    
    # Extract details using OpenAI
    extracted_details = await openai_service.extract_resume_details(parsed_text)
    
    # Store in ChromaDB
    chroma_service.add_resume_to_vector_store(parsed_text, str(user_id), str(db_resume.id))
    
    # Link to session if provided
    if session_id:
        crud.update_chat_session(db, session_id, resume_id=db_resume.id)
    
    return db_resume
