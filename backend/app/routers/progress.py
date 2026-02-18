from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(
    prefix="/progress",
    tags=["progress"]
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# define crud operations for progress/roadmap here or import from crud.py if added there.
# For now, placeholder endpoints.

@router.get("/{user_id}")
def get_user_progress(user_id: int, db: Session = Depends(get_db)):
    # Fetch progress from DB
    return {"message": "Progress data placeholder"}

@router.post("/roadmap/update")
def update_roadmap_step(step_id: int, status: str, db: Session = Depends(get_db)):
    # Update step status
    return {"message": "Roadmap step updated"}
