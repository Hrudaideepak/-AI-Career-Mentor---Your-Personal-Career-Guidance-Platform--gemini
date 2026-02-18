from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from .database import engine
from .routers import resume, chat, roadmap, analytics, career, progress, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Career Recommender")

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Career Recommender API"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(chat.router)
app.include_router(roadmap.router)
app.include_router(analytics.router)
app.include_router(career.router)
app.include_router(progress.router)
