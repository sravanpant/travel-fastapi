# main.py
from fastapi import FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from database import SessionLocal
import models

app = FastAPI()

# Pydantic models
class AccommodationCreate(BaseModel):
    hotel_id: int
    day_number: int

class TransferCreate(BaseModel):
    day_number: int
    from_location: str
    to_location: str
    transfer_type: str
    duration_hours: float

class ItineraryActivityCreate(BaseModel):
    activity_id: int
    day_number: int

class ItineraryCreate(BaseModel):
    name: str
    duration_nights: int
    region: str
    description: str
    is_recommended: bool = False
    accommodations: List[AccommodationCreate]
    transfers: List[TransferCreate]
    itinerary_activities: List[ItineraryActivityCreate]

# MCP Routes
@app.get("/mcp/recommended-itineraries/")
def get_recommended_itineraries(
    nights: int = Query(..., ge=2, le=8),
    region: Optional[str] = Query(None, enum=['Phuket', 'Krabi'])
):
    if not 2 <= nights <= 8:
        raise HTTPException(
            status_code=400,
            detail="Duration must be between 2 and 8 nights"
        )
    
    db = SessionLocal()
    try:
        query = db.query(models.Itinerary).filter(
            models.Itinerary.is_recommended == True,
            models.Itinerary.duration_nights == nights
        )
        
        if region:
            query = query.filter(models.Itinerary.region == models.Region[region.upper()])
        
        recommended = query.all()
        
        if not recommended:
            raise HTTPException(
                status_code=404,
                detail=f"No recommended itineraries found for {nights} nights"
                f"{f' in {region}' if region else ''}"
            )
        
        # Convert to dictionary with relationships
        result = []
        for itinerary in recommended:
            itinerary_dict = {
                "id": itinerary.id,
                "name": itinerary.name,
                "region": itinerary.region.value,
                "description": itinerary.description,
                "duration_nights": itinerary.duration_nights,
                "accommodations": [
                    {
                        "day_number": acc.day_number,
                        "hotel": {
                            "id": acc.hotel.id,
                            "name": acc.hotel.name,
                            "type": acc.hotel.type.value
                        }
                    } for acc in itinerary.accommodations
                ],
                "transfers": [
                    {
                        "day_number": t.day_number,
                        "from_location": t.from_location.name,
                        "to_location": t.to_location.name,
                        "transfer_type": t.transfer_type.value,
                        "duration_hours": t.duration_hours
                    } for t in itinerary.transfers
                ],
                "activities": [
                    {
                        "day_number": act.day_number,
                        "activity": {
                            "id": act.activity.id,
                            "name": act.activity.name,
                            "description": act.activity.description,
                            "duration_hours": act.activity.duration_hours
                        }
                    } for act in itinerary.activities
                ]
            }
            result.append(itinerary_dict)
        
        return result
    finally:
        db.close()

# Regular itinerary routes
@app.post("/itineraries/")
def create_itinerary(itinerary: ItineraryCreate):
    db = SessionLocal()
    try:
        # Create itinerary
        db_itinerary = models.Itinerary(
            name=itinerary.name,
            region=models.Region[itinerary.region.upper()],
            description=itinerary.description,
            duration_nights=itinerary.duration_nights,
            is_recommended=itinerary.is_recommended
        )
        db.add(db_itinerary)
        db.flush()

        # Add accommodations
        for acc in itinerary.accommodations:
            accommodation = models.Accommodation(
                itinerary_id=db_itinerary.id,
                hotel_id=acc.hotel_id,
                day_number=acc.day_number
            )
            db.add(accommodation)

        # Add transfers
        for transfer in itinerary.transfers:
            # Get location IDs based on names
            from_location = db.query(models.Location).filter_by(name=transfer.from_location).first()
            to_location = db.query(models.Location).filter_by(name=transfer.to_location).first()
            
            if not from_location or not to_location:
                raise HTTPException(status_code=400, detail="Invalid location names")

            db_transfer = models.Transfer(
                itinerary_id=db_itinerary.id,
                day_number=transfer.day_number,
                from_location_id=from_location.id,
                to_location_id=to_location.id,
                transfer_type=models.TransferType[transfer.transfer_type.upper()],
                duration_hours=transfer.duration_hours
            )
            db.add(db_transfer)

        # Add activities
        for activity in itinerary.itinerary_activities:
            db_activity = models.ItineraryActivity(
                itinerary_id=db_itinerary.id,
                activity_id=activity.activity_id,
                day_number=activity.day_number
            )
            db.add(db_activity)

        db.commit()
        return {"message": "Itinerary created successfully", "id": db_itinerary.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.get("/itineraries/{itinerary_id}")
def get_itinerary(itinerary_id: int):
    db = SessionLocal()
    try:
        itinerary = db.query(models.Itinerary).filter_by(id=itinerary_id).first()
        if not itinerary:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        # Convert to dictionary with relationships
        result = {
            "id": itinerary.id,
            "name": itinerary.name,
            "region": itinerary.region.value,
            "description": itinerary.description,
            "duration_nights": itinerary.duration_nights,
            "accommodations": [
                {
                    "day_number": acc.day_number,
                    "hotel": {
                        "id": acc.hotel.id,
                        "name": acc.hotel.name,
                        "type": acc.hotel.type.value
                    }
                } for acc in itinerary.accommodations
            ],
            "transfers": [
                {
                    "day_number": t.day_number,
                    "from_location": t.from_location.name,
                    "to_location": t.to_location.name,
                    "transfer_type": t.transfer_type.value,
                    "duration_hours": t.duration_hours
                } for t in itinerary.transfers
            ],
            "activities": [
                {
                    "day_number": act.day_number,
                    "activity": {
                        "id": act.activity.id,
                        "name": act.activity.name,
                        "description": act.activity.description,
                        "duration_hours": act.activity.duration_hours
                    }
                } for act in itinerary.activities
            ]
        }
        return result
    finally:
        db.close()