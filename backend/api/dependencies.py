from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.security import security_service
from services.interfaces import LDAPServiceAbstractClass, DatabaseServiceAbstractClass
from services.ldap_service import get_ldap_service
from services.database_service import get_database_service


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    ldap_service: LDAPServiceAbstractClass = Depends(get_ldap_service)
) -> str:
    """Get current authenticated user"""
    payload = security_service.verify_token(credentials.credentials)
    username = payload.get("sub")
    
    # Verify user still exists in LDAP
    if not ldap_service.user_exists(username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return username


def require_group(required_group: str):
    """Factory function to create group requirement dependency"""
    def _require_group(
        current_user: str = Depends(get_current_user),
        ldap_service: LDAPServiceAbstractClass = Depends(get_ldap_service)
    ):
        groups = ldap_service.get_user_groups(current_user)
        if required_group not in groups:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. {required_group} membership required."
            )
        return current_user

    return _require_group


# Group-specific dependencies
require_admin = require_group("Group_A")
require_user = require_group("Group_B")
