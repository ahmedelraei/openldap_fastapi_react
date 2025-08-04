from datetime import timedelta
from fastapi import HTTPException, status, Depends

from models.schemas import UserRegistration, UserInfo, Token
from services.interfaces import AuthServiceAbstractClass, LDAPServiceAbstractClass, DatabaseServiceAbstractClass
from core.security import security_service
from core.config import settings


class AuthService(AuthServiceAbstractClass):
    """Authentication Service implementation"""
    
    def __init__(self, ldap_service: LDAPServiceAbstractClass, db_service: DatabaseServiceAbstractClass):
        self.ldap_service = ldap_service
        self.db_service = db_service
    
    async def register_user(self, user_data: UserRegistration) -> dict:
        """Register a new user"""
        try:
            # Create user in LDAP
            self.ldap_service.create_user(user_data)
            
            # Store additional user data in MongoDB
            user_doc = {
                "username": user_data.username,
                "email": user_data.email,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
            }
            
            await self.db_service.create_user(user_doc)
            
            # Log activity
            await self.db_service.log_user_activity(
                user_data.username, 
                "User account created"
            )
            
            return {"message": "User registered successfully"}
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def authenticate_user(self, username: str, password: str) -> Token:
        """Authenticate user and return JWT token"""
        # Authenticate against LDAP
        if not self.ldap_service.authenticate_user(username, password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user groups
        groups = self.ldap_service.get_user_groups(username)
        
        # Update last login
        await self.db_service.update_user_login(username)
        
        # Log activity
        await self.db_service.log_user_activity(username, "User logged in")
        
        # Get user info for token
        user_info = await self.get_current_user(username)
        
        # Create JWT token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security_service.create_access_token(
            data={"sub": username, "groups": groups},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_info
        )
    
    async def get_current_user(self, username: str) -> UserInfo:
        """Get current user information"""
        try:
            # Get user groups from LDAP
            groups = self.ldap_service.get_user_groups(username)
            
            # Get additional user data from MongoDB
            user_doc = await self.db_service.get_user(username)
            
            if not user_doc:
                raise HTTPException(status_code=404, detail="User not found")
            
            return UserInfo(
                username=username,
                email=user_doc["email"],
                first_name=user_doc["first_name"],
                last_name=user_doc["last_name"],
                groups=groups,
                created_at=user_doc.get("created_at"),
                last_login=user_doc.get("last_login"),
                is_active=user_doc.get("is_active", True)
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# Factory function for dependency injection
def get_auth_service() -> AuthServiceAbstractClass:
    """Factory function for auth service dependency injection"""
    from services.ldap_service import get_ldap_service
    from services.database_service import get_database_service
    
    ldap_service = get_ldap_service()
    db_service = get_database_service()
    return AuthService(ldap_service, db_service)
