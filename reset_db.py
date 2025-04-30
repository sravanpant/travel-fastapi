# reset_db.py
from database import engine
import models

def reset_database():
    # Drop all tables
    models.Base.metadata.drop_all(bind=engine)
    print("All tables dropped successfully!")
    
    # Create all tables
    models.Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

if __name__ == "__main__":
    reset_database()    