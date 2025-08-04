from fastapi import APIRouter, Depends
from datetime import datetime

from models.schemas import HealthStatus
from services.interfaces import LDAPServiceAbstractClass, DatabaseServiceAbstractClass
from services.ldap_service import get_ldap_service
from services.database_service import get_database_service


router = APIRouter()


@router.get("/health", response_model=HealthStatus)
async def health_check(
    ldap_service: LDAPServiceAbstractClass = Depends(get_ldap_service),
    db_service: DatabaseServiceAbstractClass = Depends(get_database_service)
):
    """Health check endpoint"""
    services = {}
    
    # Check LDAP connection
    try:
        conn = ldap_service._get_connection()
        conn.unbind()
        services["ldap"] = "connected"
    except Exception:
        services["ldap"] = "disconnected"
    
    # Check MongoDB connection
    try:
        is_healthy = await db_service.health_check()
        services["mongodb"] = "connected" if is_healthy else "disconnected"
    except Exception:
        services["mongodb"] = "disconnected"
    
    # Determine overall status
    overall_status = "healthy" if all(
        status == "connected" for status in services.values()
    ) else "unhealthy"
    
    return HealthStatus(
        status=overall_status,
        services=services,
        timestamp=datetime.utcnow()
    )
