# Travel Itinerary System

A backend system for managing travel itineraries built with FastAPI and SQLAlchemy. This system allows creation and management of travel itineraries with features like hotel accommodations, transfers, and activities.

## Features

- Create and view travel itineraries
- Manage hotel accommodations
- Handle transfers between locations
- Schedule activities and excursions
- Get recommended itineraries based on duration and region
- Support for multiple regions (Phuket, Krabi)

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd travel-itinerary-system
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL:
```bash
# Log into PostgreSQL as postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE travel_db;
CREATE USER travel_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE travel_db TO travel_user;

# Connect to the travel_db
\c travel_db

# Grant privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO travel_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO travel_user;

# Exit PostgreSQL
\q
```

5. Update database connection:
Edit `database.py` and update the connection string:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://travel_user:your_password@localhost/travel_db"
```

## Database Setup

1. Initialize the database:
```bash
python create_tables.py
```

2. Seed the database with sample data:
```bash
python seed_data.py
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Create Itinerary
```bash
POST /itineraries/
```
Example request:
```json
{
  "name": "Custom Phuket Trip",
  "duration_nights": 3,
  "region": "Phuket",
  "description": "A custom 3-night trip to Phuket",
  "is_recommended": false,
  "accommodations": [
    {
      "hotel_id": 3,
      "day_number": 1
    },
    {
      "hotel_id": 3,
      "day_number": 2
    },
    {
      "hotel_id": 3,
      "day_number": 3
    }
  ],
  "transfers": [
    {
      "day_number": 1,
      "from_location": "Phuket Airport",
      "to_location": "Marina Phuket Resort",
      "transfer_type": "car",
      "duration_hours": 1
    },
    {
      "day_number": 4,
      "from_location": "Marina Phuket Resort",
      "to_location": "Phuket Airport",
      "transfer_type": "car",
      "duration_hours": 1
    }
  ],
  "itinerary_activities": [
    {
      "activity_id": 1,
      "day_number": 1
    },
    {
      "activity_id": 1,
      "day_number": 2
    }
  ]
}
```

### Get Itinerary
```bash
GET /itineraries/{itinerary_id}
```

### Get Recommended Itineraries
```bash
GET /mcp/recommended-itineraries/?nights={nights}&region={region}
```
Parameters:
- nights: integer (2-8)
- region: string (optional, "Phuket" or "Krabi")

## Testing the API

You can test the API using curl:

```bash
# Create new itinerary
curl -X POST http://localhost:8000/itineraries/ \
-H "Content-Type: application/json" \
-d @sample_itinerary.json

# Get specific itinerary
curl http://localhost:8000/itineraries/1

# Get recommended itineraries
curl "http://localhost:8000/mcp/recommended-itineraries/?nights=3&region=Phuket"
```

Or use the interactive API documentation at:
```
http://localhost:8000/docs
```

## Project Structure

```
travel-itinerary-system/
├── main.py             # FastAPI application and routes
├── models.py           # SQLAlchemy models
├── database.py         # Database configuration
├── seed_data.py        # Sample data seeding script
├── reset_db.py         # Database reset script
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Database Schema

- **locations**: Stores information about hotels, attractions, and airports
- **activities**: Contains available activities and excursions
- **itineraries**: Main itinerary information
- **accommodations**: Day-wise hotel accommodations
- **transfers**: Transportation between locations
- **itinerary_activities**: Activities scheduled in itineraries

## Error Handling

The API includes comprehensive error handling for:
- Invalid location references
- Missing required fields
- Invalid date ranges
- Database constraints
- Invalid enum values

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
