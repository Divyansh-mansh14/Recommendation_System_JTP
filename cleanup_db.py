from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["recommendation_system"]
users = db.users

def cleanup_duplicates():
    try:
        # Get all users
        all_users = list(users.find())
        logger.info(f"Total users in database: {len(all_users)}")

        # Find duplicate emails
        email_count = {}
        for user in all_users:
            email = user.get('email')
            if email:
                email_count[email] = email_count.get(email, 0) + 1

        # Remove duplicates
        for email, count in email_count.items():
            if count > 1:
                logger.info(f"Found {count} entries for email: {email}")
                # Keep the first entry, remove others
                first_user = users.find_one({"email": email})
                if first_user:
                    users.delete_many({
                        "email": email,
                        "_id": {"$ne": first_user["_id"]}
                    })
                    logger.info(f"Removed {count-1} duplicate entries for {email}")

        # Verify cleanup
        remaining_users = list(users.find())
        logger.info(f"Users after cleanup: {len(remaining_users)}")
        
        # List all remaining users
        logger.info("\nRemaining users:")
        for user in remaining_users:
            logger.info(f"Email: {user.get('email')}, Name: {user.get('name')}")

    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    cleanup_duplicates() 