db = db.getSiblingDB('jtp_dating_db');

// Create users collection with email index
db.createCollection('users');
db.users.createIndex({ "email": 1 }, { unique: true });

// Create profiles collection with necessary indexes
db.createCollection('profiles');
db.profiles.createIndex({ "user_id": 1 }, { unique: true });
db.profiles.createIndex({ "gender": 1 });
db.profiles.createIndex({ "age": 1 });
db.profiles.createIndex({ "location": 1 });

// Create swipes collection with compound index
db.createCollection('swipes');
db.swipes.createIndex({ "user_id": 1, "swiped_id": 1 }, { unique: true });

// Create matches collection
db.createCollection('matches');
db.matches.createIndex({ "user1_id": 1, "user2_id": 1 }, { unique: true });

// Create initial admin user
db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    {
      role: 'readWrite',
      db: 'jtp_dating_db'
    }
  ]
}); 