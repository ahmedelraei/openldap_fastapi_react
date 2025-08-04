from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from models.schemas import AdminStats, UserInfo
from services.interfaces import LDAPServiceAbstractClass, DatabaseServiceAbstractClass
from services.ldap_service import get_ldap_service
from services.database_service import get_database_service
from api.dependencies import require_admin


router = APIRouter()


@router.get("/users", response_model=List[UserInfo])
async def get_all_users(
    current_user: str = Depends(require_admin),
    ldap_service: LDAPServiceAbstractClass = Depends(get_ldap_service),
    db_service: DatabaseServiceAbstractClass = Depends(get_database_service)
):
    """Get all users - Admin only"""
    users = await db_service.get_all_users()
    user_list = []
    
    for user in users:
        try:
            groups = ldap_service.get_user_groups(user["username"])
            user_info = UserInfo(
                username=user["username"],
                email=user["email"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                groups=groups,
                created_at=user.get("created_at"),
                last_login=user.get("last_login"),
                is_active=user.get("is_active", True)
            )
            user_list.append(user_info)
        except Exception:
            # Skip users that can't be processed
            continue
    
    return user_list


@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(
    current_user: str = Depends(require_admin),
    ldap_service: LDAPServiceAbstractClass = Depends(get_ldap_service),
    db_service: DatabaseServiceAbstractClass = Depends(get_database_service)
):
    """Get admin statistics - Admin only"""
    stats = await db_service.get_admin_stats()
    
    # Count users by group from LDAP
    users = await db_service.get_all_users()
    group_a_count = 0
    group_b_count = 0
    
    for user in users:
        try:
            groups = ldap_service.get_user_groups(user["username"])
            if "Group_A" in groups:
                group_a_count += 1
            if "Group_B" in groups:
                group_b_count += 1
        except Exception:
            continue
    
    return AdminStats(
        total_users=stats["total_users"],
        group_a_users=group_a_count,
        group_b_users=group_b_count,
        active_sessions=stats["active_sessions"]
    )
