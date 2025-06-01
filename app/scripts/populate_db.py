from pymongo import MongoClient
from datetime import datetime
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Sample data with more diverse recommendations
sample_recommendations = [
    {
        "title": "Python Programming",
        "description": "Master Python programming with hands-on projects and real-world applications. Learn data structures, algorithms, and best practices.",
        "rating": 4.8,
        "category": "Programming",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Web Development Bootcamp",
        "description": "Comprehensive web development course covering HTML, CSS, JavaScript, React, and Node.js. Build modern responsive websites.",
        "rating": 4.9,
        "category": "Web Development",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Data Structures and Algorithms",
        "description": "Deep dive into essential computer science concepts. Learn to write efficient code and ace technical interviews.",
        "rating": 4.7,
        "category": "Computer Science",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Machine Learning Fundamentals",
        "description": "Introduction to machine learning algorithms and concepts. Includes practical projects using scikit-learn and TensorFlow.",
        "rating": 4.6,
        "category": "Data Science",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "DevOps Engineering",
        "description": "Learn Docker, Kubernetes, and CI/CD pipelines. Master cloud deployment and infrastructure automation.",
        "rating": 4.8,
        "category": "DevOps",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Mobile App Development",
        "description": "Build iOS and Android apps using React Native. Learn mobile UI design patterns and app deployment.",
        "rating": 4.5,
        "category": "Mobile Development",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Database Design",
        "description": "Master SQL and NoSQL databases. Learn data modeling, optimization, and best practices for scalable applications.",
        "rating": 4.7,
        "category": "Database",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Cybersecurity Basics",
        "description": "Introduction to network security, cryptography, and ethical hacking. Learn to protect systems from cyber threats.",
        "rating": 4.8,
        "category": "Security",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

async def populate_db():
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient('mongodb://localhost:27017')
        db = client['recommendation_system']
        recommendations = db['recommendations']

        # Delete existing recommendations
        await recommendations.delete_many({})
        print("Cleared existing recommendations")

        # Insert sample data
        result = await recommendations.insert_many(sample_recommendations)
        print(f"Successfully inserted {len(result.inserted_ids)} recommendations")

        # Create indexes
        await recommendations.create_index("title")
        await recommendations.create_index("category")
        await recommendations.create_index([("title", "text"), ("description", "text")])
        print("Created indexes")

        # Verify the data
        count = await recommendations.count_documents({})
        print(f"Total recommendations in database: {count}")

        # Display some sample queries
        print("\nSample queries:")
        
        # Find programming courses
        programming_courses = await recommendations.find({"category": "Programming"}).to_list(length=None)
        print(f"\nProgramming courses: {len(programming_courses)}")
        for course in programming_courses:
            print(f"- {course['title']}: {course['rating']}")

        # Find highly rated courses (rating >= 4.8)
        high_rated = await recommendations.find({"rating": {"$gte": 4.8}}).to_list(length=None)
        print(f"\nHighly rated courses (≥4.8): {len(high_rated)}")
        for course in high_rated:
            print(f"- {course['title']}: {course['rating']}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(populate_db()) 