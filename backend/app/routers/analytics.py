from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database, models
from ..services import openai_service
import json

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{user_id}")
async def get_analytics(user_id: int, db: Session = Depends(get_db)):
    # 1. Fetch latest resume
    latest_resume = crud.get_latest_resume(db, user_id)
    if not latest_resume:
        raise HTTPException(status_code=404, detail="No resume found. Please upload a resume first.")
    
    # 2. Generate Analytics via OpenAI
    try:
        analytics_json_str = await openai_service.analyze_skills(latest_resume.parsed_content)
        # Clean potential markdown
        if "```json" in analytics_json_str:
            analytics_json_str = analytics_json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in analytics_json_str:
            analytics_json_str = analytics_json_str.split("```")[1].split("```")[0].strip()

        analytics_data = json.loads(analytics_json_str)
        return analytics_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate analytics: {str(e)}")
