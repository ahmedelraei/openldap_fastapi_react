from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserRegistration(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    group: str  # "Group_A" or "Group_B"

    class Config:
        str_strip_whitespace = True
        str_min_length = 1


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        str_strip_whitespace = True
        str_min_length = 1


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserInfo"


class UserInfo(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    groups: List[str]
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: bool = True


class UserInDB(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    login_count: int = 0


class DashboardData(BaseModel):
    message: str
    data: dict


class HealthStatus(BaseModel):
    status: str
    services: dict
    timestamp: datetime


class AdminStats(BaseModel):
    total_users: int
    group_a_users: int
    group_b_users: int
    active_sessions: int


class UserActivity(BaseModel):
    timestamp: datetime
    description: str
    user_id: str


class UserProfile(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    groups: List[str]
    created_at: datetime
    last_login: Optional[datetime] = None
    login_count: int = 0
    days_active: int = 0
    last_activity: Optional[datetime] = None


# Update forward references
Token.model_rebuild()
