from abc import ABC, abstractmethod
from typing import List, Optional
from models.schemas import UserRegistration, UserInfo


class LDAPServiceAbstractClass(ABC):
    """LDAP Service Abstract Class"""
    
    @abstractmethod
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user against LDAP"""
        pass
    
    @abstractmethod
    def get_user_groups(self, username: str) -> List[str]:
        """Get user's group memberships"""
        pass
    
    @abstractmethod
    def create_user(self, user_data: UserRegistration) -> bool:
        """Create new user in LDAP"""
        pass
    
    @abstractmethod
    def user_exists(self, username: str) -> bool:
        """Check if user exists in LDAP"""
        pass


class DatabaseServiceAbstractClass(ABC):
    """Database Service Abstract Class"""
    
    @abstractmethod
    async def create_user(self, user_data: dict) -> bool:
        """Create user in database"""
        pass
    
    @abstractmethod
    async def get_user(self, username: str) -> Optional[dict]:
        """Get user from database"""
        pass
    
    @abstractmethod
    async def update_user_login(self, username: str) -> bool:
        """Update user last login timestamp"""
        pass
    
    @abstractmethod
    async def get_all_users(self) -> List[dict]:
        """Get all users from database"""
        pass
    
    @abstractmethod
    async def get_user_activities(self, username: str) -> List[dict]:
        """Get user activities from database"""
        pass


class AuthServiceAbstractClass(ABC):
    """Authentication Service Abstract Class"""
    
    @abstractmethod
    async def register_user(self, user_data: UserRegistration) -> dict:
        """Register a new user"""
        pass
    
    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> dict:
        """Authenticate user and return token"""
        pass
    
    @abstractmethod
    async def get_current_user(self, username: str) -> UserInfo:
        """Get current user information"""
        pass
