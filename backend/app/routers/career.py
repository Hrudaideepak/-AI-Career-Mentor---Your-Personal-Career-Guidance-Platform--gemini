from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database
from ..services import openai_service
import json

router = APIRouter(
    prefix="/careers",
    tags=["careers"]
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/recommendations/{user_id}")
async def get_career_recommendations(user_id: int, user_skills: str, experience_level: str, db: Session = Depends(get_db)):
    # 1. Fetch latest resume content
    # For simplicity, we just take user inputs or fetch from DB if needed.
    # Here we assume basic inputs are provided or we could fetch the last resume.
    
    # 2. Call OpenAI Service
    recommendations_json = await openai_service.generate_career_paths(user_skills, "Resume content placeholder", experience_level)
    
    # 3. Parse JSON and store in DB
    try:
        recommendations = json.loads(recommendations_json)
        saved_recs = []
        for rec in recommendations:
            rec_data = schemas.CareerRecommendationCreate(
                user_id=user_id,
                career_name=rec.get("Career Name", "Unknown"),
                reasoning=rec.get("Why it is suitable", ""),
                salary_range=rec.get("Estimated Salary Range", "")
            )
            saved_rec = crud.create_career_recommendation(db, rec_data)
            saved_recs.append(saved_rec)
        return saved_recs
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response")
