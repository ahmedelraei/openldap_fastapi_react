// MongoDB initialization script
db = db.getSiblingDB('auth_db');

// Create users collection with indexes
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "created_at": 1 });

// Create sessions collection for tracking user sessions
db.sessions.createIndex({ "username": 1 });
db.sessions.createIndex({ "created_at": 1 }, { expireAfterSeconds: 86400 }); // 24 hours

// Create logs collection for audit trails
db.logs.createIndex({ "username": 1 });
db.logs.createIndex({ "timestamp": 1 });
db.logs.createIndex({ "action": 1 });

print("Database initialization completed successfully");
