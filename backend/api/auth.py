from fastapi import APIRouter, Depends

from models.schemas import (
    UserRegistration, UserLogin, Token, UserInfo, 
)
from services.interfaces import (
    AuthServiceAbstractClass, DatabaseServiceAbstractClass
)
from services.auth_service import get_auth_service
from services.database_service import get_database_service
from api.dependencies import get_current_user, require_admin, require_user


router = APIRouter()


@router.post("/register")
async def register_user(
    user_data: UserRegistration,
    auth_service: AuthServiceAbstractClass = Depends(get_auth_service)
):
    """Register a new user"""
    return await auth_service.register_user(user_data)


@router.post("/login", response_model=Token)
async def login_user(
    user_credentials: UserLogin,
    auth_service: AuthServiceAbstractClass = Depends(get_auth_service)
):
    """Authenticate user and return JWT token"""
    return await auth_service.authenticate_user(user_credentials.username, user_credentials.password)


@router.get("/me", response_model=UserInfo)
async def get_current_user_info(
    current_user: str = Depends(get_current_user),
    auth_service: AuthServiceAbstractClass = Depends(get_auth_service)
):
    """Get current user information"""
    return await auth_service.get_current_user(current_user)


@router.post("/logout")
async def logout_user(
    current_user: str = Depends(get_current_user),
    db_service: DatabaseServiceAbstractClass = Depends(get_database_service)
):
    """Logout user (log activity)"""
    await db_service.log_user_activity(current_user, "User logged out")
    return {"message": "Successfully logged out"}
