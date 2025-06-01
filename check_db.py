from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['recommendation_system']

# Count total users
total_users = db.users.count_documents({})
print(f"\nTotal users in database: {total_users}")

# Count users by gender
male_users = db.users.count_documents({"gender": {"$regex": "^male$", "$options": "i"}})
female_users = db.users.count_documents({"gender": {"$regex": "^female$", "$options": "i"}})
other_users = db.users.count_documents({"gender": {"$regex": "^other$", "$options": "i"}})

print(f"\nUsers by gender:")
print(f"Male users: {male_users}")
print(f"Female users: {female_users}")
print(f"Other users: {other_users}")

# Get all swipes
swipes = list(db.swipes.find())
print(f"\nTotal swipes in database: {len(swipes)}")

# Sample query for a male user looking for female profiles
sample_query = {
    "gender": {"$regex": "^female$", "$options": "i"}
}
available_females = db.users.count_documents(sample_query)
print(f"\nAvailable female profiles: {available_females}")

# Print first few profiles as a sample
print("\nSample profiles:")
for profile in db.users.find().limit(5):
    print(f"ID: {profile['_id']}")
    print(f"Name: {profile.get('name', 'N/A')}")
    print(f"Gender: {profile.get('gender', 'N/A')}")
    print(f"Preferred Gender: {profile.get('preferred_gender', 'N/A')}")
    print("-" * 50) 