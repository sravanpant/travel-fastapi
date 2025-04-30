# seed_data.py
from database import SessionLocal
import models

def seed_database():
    db = SessionLocal()
    
    try:
        # Create locations
        phuket_airport = models.Location(
            name="Phuket Airport",
            type=models.LocationType.AIRPORT,
            region=models.Region.PHUKET,
            description="Phuket International Airport",
            latitude=8.1132,
            longitude=98.3169
        )
        
        marina_phuket = models.Location(
            name="Marina Phuket Resort",
            type=models.LocationType.HOTEL,
            region=models.Region.PHUKET,
            description="Luxury beachfront resort",
            latitude=7.8825,
            longitude=98.2910
        )
        
        krabi_resort = models.Location(
            name="Krabi Resort",
            type=models.LocationType.HOTEL,
            region=models.Region.KRABI,
            description="Beachfront resort in Krabi",
            latitude=8.0533,
            longitude=98.9198
        )

        phi_phi = models.Location(
            name="Phi Phi Islands",
            type=models.LocationType.ATTRACTION,
            region=models.Region.PHUKET,
            description="Famous island group",
            latitude=7.7407,
            longitude=98.7784
        )

        db.add_all([phuket_airport, marina_phuket, krabi_resort, phi_phi])
        db.flush()

        # Create activities
        island_hopping = models.Activity(
            name="Phi Phi Island Hopping",
            description="Full day island hopping tour",
            region=models.Region.PHUKET,
            duration_hours=8,
            price=100.0,
            location_id=phi_phi.id
        )

        db.add(island_hopping)
        db.flush()

        # Create recommended itineraries
        for nights in range(2, 9):
            itinerary = models.Itinerary(
                name=f"Phuket {nights}-Night Adventure",
                region=models.Region.PHUKET,
                description=f"Recommended {nights}-night stay in Phuket",
                duration_nights=nights,
                is_recommended=True
            )
            db.add(itinerary)
            db.flush()

            # Add accommodations
            for day in range(1, nights + 1):
                accommodation = models.Accommodation(
                    itinerary_id=itinerary.id,
                    hotel_id=marina_phuket.id,
                    day_number=day
                )
                db.add(accommodation)

            # Add transfers
            arrival_transfer = models.Transfer(
                itinerary_id=itinerary.id,
                day_number=1,
                from_location_id=phuket_airport.id,
                to_location_id=marina_phuket.id,
                transfer_type=models.TransferType.CAR,
                duration_hours=1.0
            )
            departure_transfer = models.Transfer(
                itinerary_id=itinerary.id,
                day_number=nights + 1,
                from_location_id=marina_phuket.id,
                to_location_id=phuket_airport.id,
                transfer_type=models.TransferType.CAR,
                duration_hours=1.0
            )
            db.add_all([arrival_transfer, departure_transfer])

            # Add activities
            activity = models.ItineraryActivity(
                itinerary_id=itinerary.id,
                activity_id=island_hopping.id,
                day_number=2
            )
            db.add(activity)

        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()