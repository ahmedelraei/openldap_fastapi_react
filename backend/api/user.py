from fastapi import APIRouter, Depends, HTTPException
from typing import List

from models.schemas import UserProfile, UserActivity
from services.interfaces import LDAPServiceAbstractClass, DatabaseServiceAbstractClass
from services.ldap_service import get_ldap_service
from services.database_service import get_database_service
from api.dependencies import get_current_user


router = APIRouter()


@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: str = Depends(get_current_user),
    ldap_service: LDAPServiceAbstractClass = Depends(get_ldap_service),
    db_service: DatabaseServiceAbstractClass = Depends(get_database_service)
):
    """Get user profile"""
    user_doc = await db_service.get_user(current_user)
    groups = ldap_service.get_user_groups(current_user)
    
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserProfile(
        username=current_user,
        email=user_doc["email"],
        first_name=user_doc["first_name"],
        last_name=user_doc["last_name"],
        groups=groups,
        created_at=user_doc.get("created_at"),
        last_login=user_doc.get("last_login"),
        login_count=user_doc.get("login_count", 0),
        days_active=user_doc.get("days_active", 0),
        last_activity=user_doc.get("last_activity")
    )


@router.get("/activities", response_model=List[UserActivity])
async def get_user_activities(
    current_user: str = Depends(get_current_user),
    db_service: DatabaseServiceAbstractClass = Depends(get_database_service)
):
    """Get user activities"""
    activities = await db_service.get_user_activities(current_user)
    
    return [
        UserActivity(
            timestamp=activity["timestamp"],
            description=activity["description"],
            user_id=activity["user_id"]
        )
        for activity in activities
    ]
