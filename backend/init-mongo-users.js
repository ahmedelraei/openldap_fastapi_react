// MongoDB initialization script for default users
// This script creates the default users in MongoDB that correspond to LDAP users

print('Starting MongoDB user initialization...');

// Switch to the application database (same as in init-mongo.js)
db = db.getSiblingDB('auth_db');

// Check if users collection already has data
const existingUsersCount = db.users.countDocuments();
if (existingUsersCount > 0) {
    print(`Users collection already has ${existingUsersCount} documents. Skipping initialization.`);
} else {
    print('Creating default users in MongoDB...');
    
    // Create default users that match LDAP users
    const users = [
        {
            username: 'user1',
            email: 'user1@example.com',
            first_name: 'User',
            last_name: 'One',
            full_name: 'User One',
            is_active: true,
            created_at: new Date(),
            updated_at: new Date(),
            ldap_dn: 'uid=user1,ou=people,dc=example,dc=com',
            groups: ['Group_A'],
            role: 'admin'
        },
        {
            username: 'user2',
            email: 'user2@example.com',
            first_name: 'User',
            last_name: 'Two',
            full_name: 'User Two',
            is_active: true,
            created_at: new Date(),
            updated_at: new Date(),
            ldap_dn: 'uid=user2,ou=people,dc=example,dc=com',
            groups: ['Group_B'],
            role: 'user'
        }
    ];
    
    // Insert users
    const result = db.users.insertMany(users);
    print(`Created ${result.insertedIds.length} users in MongoDB`);
    
    // Additional indexes for LDAP integration
    db.users.createIndex({ ldap_dn: 1 }, { unique: true });
    db.users.createIndex({ groups: 1 });
    db.users.createIndex({ role: 1 });
    
    print('Created additional indexes for LDAP integration');
    
    // Verify users were created
    const finalCount = db.users.countDocuments();
    print(`Total users in database: ${finalCount}`);
    
    // Display created users
    print('Created users:');
    db.users.find({}, { username: 1, email: 1, role: 1, groups: 1 }).forEach(user => {
        print(`- ${user.username} (${user.email}) - Role: ${user.role}, Groups: ${user.groups.join(', ')}`);
    });
}

print('MongoDB user initialization completed!');
