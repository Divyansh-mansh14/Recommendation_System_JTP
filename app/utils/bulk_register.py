import pandas as pd
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine
from ..models import User, Base
import json

def register_users_from_csv(csv_path: str):
    """
    Register users from a CSV file.
    Expected CSV columns:
    - email
    - password (optional, will use 'password123' if not provided)
    - name
    - age
    - gender (male/female/other)
    - religion
    - location
    - education_level
    - profession
    - smoking (true/false)
    - drinking (true/false)
    - diet
    - hobbies (comma-separated list)
    - languages (comma-separated list)
    """
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Create database session
        db = SessionLocal()
        
        # Track statistics
        total_users = 0
        skipped_users = 0
        registered_users = 0
        
        # Process each row
        for _, row in df.iterrows():
            try:
                total_users += 1
                
                # Check if user already exists
                existing_user = db.query(User).filter(User.email == row['email']).first()
                if existing_user:
                    print(f"Skipping user {row['name']} ({row['email']}) - already exists")
                    skipped_users += 1
                    continue
                
                # Convert hobbies and languages from string to list if they exist
                hobbies = row.get('hobbies', '').split(',') if pd.notna(row.get('hobbies')) else []
                languages = row.get('languages', '').split(',') if pd.notna(row.get('languages')) else []
                
                # Clean the lists
                hobbies = [h.strip() for h in hobbies if h.strip()]
                languages = [l.strip() for l in languages if l.strip()]
                
                # Create user object
                user = User(
                    email=row['email'],
                    hashed_password=row.get('password', 'password123'),  # In production, hash this!
                    name=row['name'],
                    age=int(row['age']),
                    gender=row['gender'].lower(),
                    preferred_gender=row.get('preferred_gender', row['gender']).lower(),  # Default to same gender if not specified
                    religion=row.get('religion', ''),
                    location=row['location'],
                    education_level=row.get('education_level', ''),
                    profession=row.get('profession', ''),
                    smoking=bool(row.get('smoking', False)),
                    drinking=bool(row.get('drinking', False)),
                    diet=row.get('diet', ''),
                    hobbies=hobbies,
                    languages=languages,
                    is_active=True
                )
                
                # Add to database
                db.add(user)
                db.commit()
                print(f"Successfully registered user: {row['name']} ({row['email']})")
                registered_users += 1
                
            except Exception as e:
                print(f"Error registering user {row.get('name', 'Unknown')}: {str(e)}")
                db.rollback()
                continue
        
        print(f"\nBulk registration summary:")
        print(f"Total users in CSV: {total_users}")
        print(f"Successfully registered: {registered_users}")
        print(f"Skipped (already exist): {skipped_users}")
        print(f"Failed to register: {total_users - registered_users - skipped_users}")
        
    except Exception as e:
        print(f"Error during bulk registration: {str(e)}")
    
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python -m app.utils.bulk_register <path_to_csv>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    register_users_from_csv(csv_path) 