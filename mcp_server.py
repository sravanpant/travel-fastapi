# mcp_server.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models

router = APIRouter()

@router.get("/recommended-itineraries/{nights}")
def get_recommended_itineraries(nights: int):
    if not 2 <= nights <= 8:
        raise HTTPException(status_code=400, detail="Duration must be between 2 and 8 nights")
    
    db = SessionLocal()
    try:
        recommended = db.query(models.Itinerary).filter(
            models.Itinerary.duration_nights == nights,
            models.Itinerary.is_recommended == True
        ).all()
        return recommended
    finally:
        db.close()