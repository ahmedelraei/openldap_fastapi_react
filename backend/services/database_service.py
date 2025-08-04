from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from datetime import datetime

from core.config import settings
from services.interfaces import DatabaseServiceAbstractClass


class MongoDBService(DatabaseServiceAbstractClass):
    """MongoDB Service"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database = None
    
    async def _get_database(self):
        """Get database connection"""
        if self.client is None:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.database = self.client[settings.MONGODB_DATABASE]
        return self.database
    
    async def create_user(self, user_data: dict) -> bool:
        """Create user in database"""
        try:
            db = await self._get_database()
            user_doc = {
                **user_data,
                "created_at": datetime.utcnow(),
                "is_active": True,
                "login_count": 0
            }
            
            await db.users.insert_one(user_doc)
            return True
        except Exception:
            return False
    
    async def get_user(self, username: str) -> Optional[dict]:
        """Get user from database"""
        try:
            db = await self._get_database()
            return await db.users.find_one({"username": username})
        except Exception:
            return None
    
    async def update_user_login(self, username: str) -> bool:
        """Update user last login timestamp"""
        try:
            db = await self._get_database()
            update_data = {
                "$set": {"last_login": datetime.utcnow()},
                "$inc": {"login_count": 1}
            }
            result = await db.users.update_one(
                {"username": username}, 
                update_data
            )
            return result.modified_count > 0
        except Exception:
            return False
    
    async def get_all_users(self) -> List[dict]:
        """Get all users from database"""
        try:
            db = await self._get_database()
            cursor = db.users.find({}, {"_id": 0})
            return await cursor.to_list(length=None)
        except Exception:
            return []
    
    async def get_user_activities(self, username: str) -> List[dict]:
        """Get user activities from database"""
        try:
            db = await self._get_database()
            cursor = db.user_activities.find(
                {"user_id": username},
                {"_id": 0}
            ).sort("timestamp", -1).limit(10)
            return await cursor.to_list(length=10)
        except Exception:
            return []
    
    async def log_user_activity(self, username: str, description: str) -> bool:
        """Log user activity"""
        try:
            db = await self._get_database()
            activity = {
                "user_id": username,
                "description": description,
                "timestamp": datetime.utcnow()
            }
            await db.user_activities.insert_one(activity)
            return True
        except Exception:
            return False
    
    async def get_admin_stats(self) -> dict:
        """Get admin statistics"""
        try:
            db = await self._get_database()
            
            # Count total users
            total_users = await db.users.count_documents({})
            
            # Count active sessions
            yesterday = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            active_sessions = await db.users.count_documents({
                "last_login": {"$gte": yesterday}
            })
            
            return {
                "total_users": total_users,
                "group_a_users": 0,  # Will be calculated from LDAP
                "group_b_users": 0,  # Will be calculated from LDAP
                "active_sessions": active_sessions
            }
        except Exception:
            return {
                "total_users": 0,
                "group_a_users": 0,
                "group_b_users": 0,
                "active_sessions": 0
            }
    
    async def health_check(self) -> bool:
        """Check MongoDB connection health"""
        try:
            db = await self._get_database()
            await db.command("ping")
            return True
        except Exception:
            return False


def get_database_service() -> DatabaseServiceAbstractClass:
    """Factory function for database service"""
    return MongoDBService()
