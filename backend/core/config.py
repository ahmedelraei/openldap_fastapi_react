import os
from typing import List


class Settings:
    """Application settings following the Dependency Inversion Principle"""
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # LDAP Configuration
    LDAP_HOST: str = os.getenv("LDAP_HOST", "openldap")
    LDAP_PORT: int = int(os.getenv("LDAP_PORT", "1389"))
    LDAP_BASE_DN: str = os.getenv("LDAP_BASE_DN", "dc=example,dc=com")
    LDAP_ADMIN_DN: str = os.getenv("LDAP_ADMIN_DN", "cn=admin,dc=example,dc=com")
    LDAP_ADMIN_PASSWORD: str = os.getenv("LDAP_ADMIN_PASSWORD", "admin123")
    LDAP_USERS_OU: str = "ou=people"
    LDAP_GROUPS_OU: str = "ou=groups"
    
    # MongoDB Configuration
    MONGODB_URL: str = os.getenv(
        "MONGODB_URL", 
        "mongodb://admin:admin123@mongo:27017/auth_db?authSource=admin"
    )
    MONGODB_DATABASE: str = os.getenv("MONGO_INITDB_DATABASE", "auth_db")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://frontend:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Application Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "OpenLDAP Authentication API"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Security Configuration
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    class Config:
        case_sensitive = True


settings = Settings()
