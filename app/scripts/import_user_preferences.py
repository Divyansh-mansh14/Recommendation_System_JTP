import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import os
from ..utils.image_mapping import get_random_image_for_gender

# File path
CSV_PATH = "C:/Users/Lenovo/OneDrive/Desktop/Recommendation System for JTP/app/matching_users_with_preferences_dataset.csv"

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['recommendation_system']
users_collection = db['users']

def import_user_preferences():
    try:
        # Read CSV file
        print(f"Reading CSV file from: {CSV_PATH}")
        df = pd.read_csv(CSV_PATH)
        print(f"Found {len(df)} records in CSV file")

        # Convert DataFrame to list of dictionaries
        records = df.to_dict('records')

        # Track used images to avoid duplicates
        used_images = set()

        # Add timestamps and profile images to each record
        current_time = datetime.utcnow()
        for record in records:
            record['created_at'] = current_time
            record['updated_at'] = current_time
            
            # Assign profile image based on gender
            profile_image = get_random_image_for_gender(record['gender'], used_images)
            record['profile_image'] = profile_image
            used_images.add(profile_image)

        # Clear existing data
        users_collection.delete_many({})
        print("Cleared existing user data")

        # Insert new data
        result = users_collection.insert_many(records)
        print(f"Successfully inserted {len(result.inserted_ids)} user records")

        # Create indexes for better query performance
        users_collection.create_index("gender")
        users_collection.create_index("age")
        users_collection.create_index("preferred_gender")
        print("Created indexes")

        # Display some sample data
        print("\nSample data in database:")
        for user in users_collection.find().limit(3):
            print(f"User: {user}")

    except FileNotFoundError:
        print(f"Error: CSV file not found at {CSV_PATH}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    import_user_preferences() 